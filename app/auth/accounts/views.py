import json
import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings as django_settings
from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .forms import InscriptionForm
from .email_utils import send_activation_email, email_configure
from . import google_auth
from .sync_utilisateur import ensure_utilisateur
from .competences_utils import (
    competences_par_niveau_json,
    sync_points_faibles,
    sync_points_forts,
)
from .db_guard import SETUP_MESSAGE, require_metier_schema
from .db_setup import metier_schema_ready

User = get_user_model()
from app.matching.models import (
    PointsForts, PointsFaibles, Competences,
    Utilisateurs, Disponibilites, Matching
)


def _sync_disponibilites(user_id, post):
    Disponibilites.objects.filter(utilisateur_id=user_id).delete()
    jours = post.getlist('dispo_jour')
    debuts = post.getlist('dispo_debut')
    fins = post.getlist('dispo_fin')
    for jour, debut, fin in zip(jours, debuts, fins):
        jour = (jour or '').strip()
        if jour and debut and fin:
            Disponibilites.objects.create(
                utilisateur_id=user_id,
                jour=jour,
                heure_debut=debut,
                heure_fin=fin,
            )


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            try:
                ensure_utilisateur(user)
            except Exception as e:
                print(f"Sync utilisateurs: {e}")
            points_forts = request.POST.getlist('points_forts')
            points_faibles = request.POST.getlist('points_faibles')
            for nom_comp in points_forts:
                comp = Competences.objects.filter(nom=nom_comp).first()
                if comp:
                    try:
                        PointsForts.objects.get_or_create(
                            competences_id=comp.id,
                            utilisateurs_id=user.id
                        )
                    except Exception:
                        pass
            for nom_comp in points_faibles:
                comp = Competences.objects.filter(nom=nom_comp).first()
                if comp:
                    try:
                        PointsFaibles.objects.get_or_create(
                            competences_id=comp.id,
                            utilisateurs_id=user.id
                        )
                    except Exception:
                        pass
            try:
                send_activation_email(request, user)
                django_messages.success(
                    request,
                    "Compte créé ! Consultez votre email pour activer votre inscription.",
                )
            except Exception as e:
                django_messages.warning(
                    request,
                    f"Compte créé mais l'email n'a pas pu être envoyé : {e}",
                )
            request.session['pending_activation_email'] = user.email
            return redirect('inscription_confirmation')
        else:
            print(form.errors)
    else:
        form = InscriptionForm()
    return render(request, 'account/register.html', {
        'form': form,
        'google_enabled': google_auth.google_oauth_enabled(),
    })


def connexion(request):
    context = {'google_enabled': google_auth.google_oauth_enabled()}
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password')
        pending = User.objects.filter(email=email).first()
        if pending and not pending.is_active:
            context['error'] = (
                "Votre compte n'est pas encore activé. "
                "Vérifiez votre email ou renvoyez le lien de confirmation."
            )
            context['inactive_email'] = email
            return render(request, 'account/login.html', context)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                ensure_utilisateur(user)
            except Exception:
                pass
            return redirect('dashboard')
        context['error'] = 'Email ou mot de passe incorrect.'
        return render(request, 'account/login.html', context)
    return render(request, 'account/login.html', context)


def inscription_confirmation(request):
    email = request.session.get('pending_activation_email', '')
    return render(request, 'account/inscription_confirmation.html', {
        'email': email,
        'email_configured': email_configure(),
    })


def renvoyer_activation(request):
    if request.method != 'POST':
        return redirect('connexion')
    email = (request.POST.get('email') or '').strip().lower()
    user = User.objects.filter(email=email, is_active=False).first()
    if not user:
        django_messages.info(request, "Aucun compte en attente trouvé pour cet email.")
        return redirect('connexion')
    try:
        send_activation_email(request, user)
        django_messages.success(request, "Email de confirmation renvoyé.")
    except Exception as e:
        django_messages.error(request, f"Impossible d'envoyer l'email : {e}")
    request.session['pending_activation_email'] = email
    return redirect('inscription_confirmation')


def confirmer_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        try:
            ensure_utilisateur(user)
        except Exception:
            pass
        django_messages.success(request, "Email confirmé ! Vous pouvez vous connecter.")
        return redirect('connexion')
    django_messages.error(request, "Lien de confirmation invalide ou expiré.")
    return redirect('connexion')


def google_login(request):
    if not google_auth.google_oauth_enabled():
        django_messages.error(request, "La connexion Google n'est pas configurée.")
        return redirect('connexion')
    return redirect(google_auth.build_google_auth_url(request))


def google_callback(request):
    if not google_auth.google_oauth_enabled():
        return redirect('connexion')
    state = request.GET.get('state')
    if not state or state != request.session.get('google_oauth_state'):
        django_messages.error(request, "Session Google invalide. Réessayez.")
        return redirect('connexion')
    request.session.pop('google_oauth_state', None)
    code = request.GET.get('code')
    if not code:
        django_messages.error(request, "Connexion Google annulée.")
        return redirect('connexion')
    try:
        profile = google_auth.fetch_google_profile(code, request)
        user, created = google_auth.get_or_create_google_user(profile)
        ensure_utilisateur(user)
        login(request, user)
        if created:
            django_messages.info(
                request,
                "Compte Google créé. Complétez votre filière et niveau dans votre profil.",
            )
            return redirect('profil')
        django_messages.success(request, f"Bienvenue, {user.prenom} !")
        return redirect('dashboard')
    except Exception as e:
        django_messages.error(request, f"Erreur Google : {e}")
        return redirect('connexion')


def deconnexion(request):
    logout(request)
    django_messages.info(request, "Vous avez été déconnecté.")
    return redirect('connexion')


def accueil(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


@login_required
def profil(request):
    user = request.user
    if request.method == 'POST':
        if not metier_schema_ready():
            django_messages.error(request, SETUP_MESSAGE)
            return redirect('profil')
        user.nom = request.POST.get('nom', user.nom).strip()
        user.prenom = request.POST.get('prenom', user.prenom).strip()
        user.filiere = request.POST.get('filiere', user.filiere).strip()
        user.niveau = request.POST.get('niveau', user.niveau).strip()
        user.bio = request.POST.get('bio', '')
        user.centre_interet = request.POST.get('centre_interet', user.centre_interet or '')
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            ext = os.path.splitext(photo.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                safe_name = f"{uuid.uuid4().hex}{ext}"
                media_dir = os.path.join(django_settings.BASE_DIR, 'media', 'profils')
                os.makedirs(media_dir, exist_ok=True)
                with open(os.path.join(media_dir, safe_name), 'wb') as f:
                    for chunk in photo.chunks():
                        f.write(chunk)
                user.photo = f'profils/{safe_name}'
        user.save()
        try:
            ensure_utilisateur(user)
            sync_points_forts(user.id, request.POST.getlist('points_forts'))
            sync_points_faibles(user.id, request.POST.getlist('points_faibles'))
            _sync_disponibilites(user.id, request.POST)
        except Exception as e:
            django_messages.error(
                request,
                "Impossible d'enregistrer compétences ou disponibilités. "
                f"Vérifiez que la base métier est chargée (schema.sql). Détail : {e}",
            )
            return redirect('profil')
        django_messages.success(request, "Profil mis à jour !")
        return redirect('profil')

    if not metier_schema_ready():
        django_messages.error(request, SETUP_MESSAGE)
        return render(request, 'account/profile.html', {
            'user': user,
            'points_forts': [],
            'points_faibles': [],
            'disponibilites': [],
            'pf_selectionnes_json': '[]',
            'pfa_selectionnes_json': '[]',
            'competences_par_niveau_json': '{}',
            'schema_missing': True,
        })

    try:
        ensure_utilisateur(user)
    except Exception as e:
        django_messages.warning(
            request,
            f"Synchronisation du profil métier incomplète : {e}",
        )

    points_forts = PointsForts.objects.filter(
        utilisateurs_id=user.id
    ).select_related('competences')
    points_faibles = PointsFaibles.objects.filter(
        utilisateurs_id=user.id
    ).select_related('competences')
    disponibilites = Disponibilites.objects.filter(utilisateur_id=user.id)
    pf_selectionnes = set(points_forts.values_list('competences__nom', flat=True))
    pfa_selectionnes = set(points_faibles.values_list('competences__nom', flat=True))

    if not Competences.objects.exists():
        django_messages.warning(
            request,
            "Aucune compétence en base. Exécutez : py manage.py setup_metier",
        )

    return render(request, 'account/profile.html', {
        'user': user,
        'points_forts': points_forts,
        'points_faibles': points_faibles,
        'disponibilites': disponibilites,
        'pf_selectionnes_json': json.dumps(list(pf_selectionnes), ensure_ascii=False),
        'pfa_selectionnes_json': json.dumps(list(pfa_selectionnes), ensure_ascii=False),
        'competences_par_niveau_json': competences_par_niveau_json(),
        'schema_missing': False,
    })


@login_required
def offres_demandes(request):
    from app.offres.views import liste_offres
    return liste_offres(request)


@login_required
def matchings(request):
    from app.matching.views import recherche_mentor
    return recherche_mentor(request)


@login_required
def vue_messagerie(request):
    from app.messagerie.views import liste_conversations
    return liste_conversations(request)


@login_required
def sessions(request):
    return render(request, 'sessions.html', {'user': request.user})


@login_required
def notifications(request):
    from app.messagerie.views import notifications as messagerie_notifications
    return messagerie_notifications(request)


@login_required
def vue_parametres(request):
    if request.method == 'POST':
        password_actuel = request.POST.get('password_actuel', '').strip()
        password_nouveau = request.POST.get('password_nouveau', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        if password_actuel and password_nouveau:
            user_auth = authenticate(
                request, username=request.user.email, password=password_actuel
            )
            if user_auth:
                if password_nouveau == password_confirm:
                    request.user.set_password(password_nouveau)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    django_messages.success(request, "Mot de passe mis à jour !")
                else:
                    django_messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
            else:
                django_messages.error(request, "Mot de passe actuel incorrect.")
    return render(request, 'account/settings.html', {'user': request.user})


@login_required
def dashboard(request):
    try:
        ensure_utilisateur(request.user)
        user_id = request.user.id
        nb_matchings = (
            Matching.objects.filter(mentor_id=user_id).count() +
            Matching.objects.filter(mentore_id=user_id).count()
        )
        nb_mentors = Matching.objects.filter(
            Q(mentor_id=user_id) | Q(mentore_id=user_id),
            statut='accepte',
        ).count()
        from app.messagerie.utils import messages_utilisateur, conversations_utilisateur
        msgs = messages_utilisateur(user_id)
        nb_messages = msgs.filter(expediteur_id=user_id).count()
        nb_non_lus = msgs.filter(lu=False).exclude(expediteur_id=user_id).count()
        nb_sessions = conversations_utilisateur(user_id).count()
    except Exception:
        nb_matchings = nb_messages = nb_non_lus = nb_sessions = nb_mentors = 0

    return render(request, 'dashboard.html', {
        'user': request.user,
        'nb_matchings': nb_matchings,
        'nb_messages': nb_messages,
        'nb_sessions': nb_sessions,
        'nb_mentors': nb_mentors,
        'nb_non_lus': nb_non_lus,
    })

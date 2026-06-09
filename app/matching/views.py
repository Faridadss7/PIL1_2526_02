from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from app.auth.accounts.db_guard import require_metier_schema
from app.auth.accounts.sync_utilisateur import ensure_utilisateur
from .models import (
    Utilisateurs, PointsFaibles, PointsForts,
    Disponibilites, Matching, Conversations, Competences
)


@login_required
def recherche_mentor(request):
    """Affiche le bouton de lancement ou les résultats selon ?lancer=1."""
    if not require_metier_schema(request):
        return render(request, 'matching/matchings.html', {'user': request.user})

    try:
        ensure_utilisateur(request.user)
    except Exception as e:
        django_messages.error(request, f"Profil non synchronisé : {e}")
        return render(request, 'matching/matchings.html', {'user': request.user})

    resultats = None
    message = None
    lancer = request.GET.get('lancer') == '1'

    if lancer:
        try:
            utilisateur = Utilisateurs.objects.get(id=request.user.id)
            points_faibles = list(PointsFaibles.objects.filter(
                utilisateurs=utilisateur
            ).values_list('competences_id', flat=True))

            if not points_faibles:
                message = "Ajoutez des points faibles à votre profil pour trouver des mentors."
            else:
                mentors_potentiels = Utilisateurs.objects.filter(
                    points_forts__competences_id__in=points_faibles
                ).exclude(id=utilisateur.id).distinct()

                resultats = []
                for mentor in mentors_potentiels:
                    pf_mentor = list(PointsForts.objects.filter(
                        utilisateurs=mentor
                    ).values_list('competences_id', flat=True))
                    communs = set(points_faibles) & set(pf_mentor)
                    score_comp = (len(communs) / len(points_faibles)) * 50

                    dispo_user = list(Disponibilites.objects.filter(
                        utilisateur=utilisateur
                    ).values_list('jour', flat=True))
                    dispo_mentor = list(Disponibilites.objects.filter(
                        utilisateur=mentor
                    ).values_list('jour', flat=True))
                    dispo_communes = set(dispo_user) & set(dispo_mentor)
                    score_dispo = (len(dispo_communes) / len(dispo_user)) * 30 if dispo_user else 0

                    score_filiere = 20 if mentor.filiere == utilisateur.filiere else 0
                    score_total = round(score_comp + score_dispo + score_filiere, 2)

                    noms_communs = list(Competences.objects.filter(
                        id__in=communs
                    ).values_list('nom', flat=True))

                    resultats.append({
                        'mentor': mentor,
                        'score': score_total,
                        'communs': noms_communs,
                        'dispo_communes': list(dispo_communes),
                    })
                resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)
        except Utilisateurs.DoesNotExist:
            django_messages.error(request, "Profil non trouvé. Veuillez compléter votre profil.")
        except Exception as e:
            django_messages.error(request, f"Erreur lors du calcul : {str(e)}")

    return render(request, 'matching/matchings.html', {
        'resultats': resultats,
        'message': message,
        'user': request.user,
    })


@login_required
def calculer_matching(request):
    return redirect(reverse('matchings') + '?lancer=1')


@login_required
def detail_mentor(request, mentor_id):
    try:
        mentor = get_object_or_404(Utilisateurs, id=mentor_id)
        points_forts = PointsForts.objects.filter(
            utilisateurs=mentor
        ).select_related('competences')
        disponibilites = Disponibilites.objects.filter(utilisateur=mentor)
        return render(request, 'matching/matchings.html', {
            'mentor': mentor,
            'points_forts': points_forts,
            'disponibilites': disponibilites,
            'user': request.user,
        })
    except Http404:
        raise
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
        return redirect('matchings')


@login_required
def accepter_matching(request, matching_id):
    try:
        matching = get_object_or_404(Matching, id=matching_id)
        if matching.mentor_id != request.user.id and matching.mentore_id != request.user.id:
            django_messages.error(request, "Accès non autorisé.")
            return redirect('matchings')
        matching.statut = 'accepte'
        matching.save()
        if not Conversations.objects.filter(matching=matching).exists():
            Conversations.objects.create(matching=matching)
        django_messages.success(request, "Correspondance acceptée ! Une conversation a été créée.")
        return redirect('messages')
    except Http404:
        raise
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
        return redirect('matchings')


@login_required
def refuser_matching(request, matching_id):
    try:
        matching = get_object_or_404(Matching, id=matching_id)
        if matching.mentor_id != request.user.id and matching.mentore_id != request.user.id:
            django_messages.error(request, "Accès non autorisé.")
            return redirect('mes_matchings')
        matching.statut = 'refuse'
        matching.save()
        django_messages.info(request, "Correspondance refusée.")
    except Http404:
        raise
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
    return redirect('mes_matchings')


@login_required
def mes_matchings(request):
    """Matchings en attente (utilisateur mentor) et matchings acceptés (mentor ou mentoré)."""
    try:
        ensure_utilisateur(request.user)
    except Exception as e:
        django_messages.error(request, f"Profil non synchronisé : {e}")
        return redirect('profil')

    try:
        matchings_en_attente = Matching.objects.filter(
            mentor_id=request.user.id,
            statut='en_attente'
        ).select_related('mentore').order_by('-date_matching')
        matchings_acceptes = Matching.objects.filter(
            Q(mentor_id=request.user.id) | Q(mentore_id=request.user.id),
            statut='accepte'
        ).select_related('mentor', 'mentore').order_by('-date_matching')
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
        matchings_en_attente = Matching.objects.none()
        matchings_acceptes = Matching.objects.none()

    return render(request, 'matching/matchings.html', {
        'matchings_en_attente': matchings_en_attente,
        'matchings_acceptes': matchings_acceptes,
        'user': request.user,
        'vue_matchings': True,
    })

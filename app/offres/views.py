from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from app.auth.accounts.db_guard import require_metier_schema
from app.auth.accounts.sync_utilisateur import ensure_utilisateur
from app.matching.models import OffresMentorat, Competences, Matching


def _offres_vide(user):
    return {
        'offres': [],
        'competences': [],
        'user': user,
    }


@login_required
def liste_offres(request):
    if not require_metier_schema(request):
        return render(request, 'offres/Offres&Demandes.html', _offres_vide(request.user))

    try:
        ensure_utilisateur(request.user)
    except Exception as e:
        django_messages.error(request, f"Profil non synchronisé : {e}")
        return render(request, 'offres/Offres&Demandes.html', _offres_vide(request.user))

    matiere = request.GET.get('matiere', '')
    format_recherche = request.GET.get('format', '')
    offres = OffresMentorat.objects.filter(statut='active').select_related(
        'competences', 'utilisateurs'
    )
    if matiere:
        offres = offres.filter(competences__nom__icontains=matiere)
    if format_recherche:
        offres = offres.filter(format=format_recherche)
    offres = offres.order_by('-date_publication')
    return render(request, 'offres/Offres&Demandes.html', {
        'offres': offres,
        'competences': Competences.objects.all(),
        'user': request.user,
        'matiere': matiere,
        'format_recherche': format_recherche,
    })


@login_required
def detail_offre(request, offre_id):
    offre = get_object_or_404(
        OffresMentorat.objects.select_related('competences', 'utilisateurs'),
        id=offre_id,
    )
    return render(request, 'offres/Offres&Demandes.html', {
        'offre': offre,
        'competences': Competences.objects.all(),
        'user': request.user,
    })


@login_required
def publier_offre(request):
    if request.method == 'POST':
        comp_id = request.POST.get('competence_id')
        type_offre = request.POST.get('type')
        format_offre = request.POST.get('format')
        if not comp_id or not type_offre or not format_offre:
            django_messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('offres_demandes')
        try:
            utilisateur = ensure_utilisateur(request.user)
            OffresMentorat.objects.create(
                utilisateurs=utilisateur,
                type=type_offre,
                competences_id=comp_id,
                format=format_offre,
                description=request.POST.get('description', ''),
                statut='active'
            )
            django_messages.success(request, "Offre publiée avec succès !")
        except Exception as e:
            django_messages.error(request, f"Erreur : {str(e)}")
    return redirect('offres_demandes')


@login_required
def repondre_offre(request, offre_id):
    offre = get_object_or_404(OffresMentorat, id=offre_id)
    if offre.utilisateurs_id == request.user.id:
        django_messages.error(request, "Vous ne pouvez pas répondre à votre propre offre.")
        return redirect('offres_demandes')
    try:
        utilisateur = ensure_utilisateur(request.user)
        if offre.type == 'offre':
            Matching.objects.create(
                mentor=offre.utilisateurs,
                mentore=utilisateur,
                statut='en_attente'
            )
        else:
            Matching.objects.create(
                mentor=utilisateur,
                mentore=offre.utilisateurs,
                statut='en_attente'
            )
        django_messages.success(request, "Réponse envoyée ! En attente de confirmation.")
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
    return redirect('offres_demandes')


@login_required
def mes_offres(request):
    try:
        ensure_utilisateur(request.user)
    except Exception as e:
        django_messages.error(request, f"Profil non synchronisé : {e}")
        return redirect('profil')

    offres = OffresMentorat.objects.filter(
        utilisateurs_id=request.user.id
    ).select_related('competences').order_by('-date_publication')
    return render(request, 'offres/Offres&Demandes.html', {
        'offres': offres,
        'competences': Competences.objects.all(),
        'user': request.user,
        'mes_offres_vue': True,
    })


@login_required
def changer_statut(request, offre_id):
    if request.method != 'POST':
        return redirect('mes_offres')
    offre = get_object_or_404(
        OffresMentorat, id=offre_id, utilisateurs_id=request.user.id
    )
    offre.statut = 'inactive' if offre.statut == 'active' else 'active'
    offre.save()
    django_messages.success(request, "Statut de l'offre mis à jour.")
    return redirect('mes_offres')

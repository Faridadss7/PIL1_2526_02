from django.shortcuts import render, redirect, get_object_or_404
from .models import OffresMentorat, Utilisateurs, Competences, Matching


def liste_offres(request):
    # Récupérer l'utilisateur connecté
    utilisateur_id = request.session.get('user_id')
    if not utilisateur_id:
        return redirect('login')

    # Récupérer les filtres de recherche
    matiere = request.GET.get('matiere')
    format_recherche = request.GET.get('format')

    # Récupérer toutes les offres actives
    offres = OffresMentorat.objects.filter(statut='active')

    # Filtrer par matière si demandé
    if matiere:
        offres = offres.filter(competences__nom__icontains=matiere)

    # Filtrer par format si demandé
    if format_recherche:
        offres = offres.filter(format=format_recherche)

    return render(request, 'offres/liste_offres.html', {
        'offres': offres,
        'competences': Competences.objects.all(),
    })


def publier_offre(request):
    # Récupérer l'utilisateur connecté
    utilisateur_id = request.session.get('user_id')
    if not utilisateur_id:
        return redirect('login')

    if request.method == 'POST':
        utilisateur = get_object_or_404(Utilisateurs, id=utilisateur_id)
        OffresMentorat.objects.create(
            utilisateurs=utilisateur,
            type=request.POST.get('type'),
            competences_id=request.POST.get('competence_id'),
            format=request.POST.get('format'),
            description=request.POST.get('description'),
            statut='active'
        )
        return redirect('liste_offres')

    return render(request, 'offres/publier_offre.html', {
        'competences': Competences.objects.all(),
    })


def detail_offre(request, offre_id):
    # Récupérer l'utilisateur connecté
    utilisateur_id = request.session.get('user_id')
    if not utilisateur_id:
        return redirect('login')

    offre = get_object_or_404(OffresMentorat, id=offre_id)

    return render(request, 'offres/detail_offre.html', {
        'offre': offre,
    })


def repondre_offre(request, offre_id):
    # Récupérer l'utilisateur connecté
    utilisateur_id = request.session.get('user_id')
    if not utilisateur_id:
        return redirect('login')

    offre = get_object_or_404(OffresMentorat, id=offre_id)

    # Créer un matching en attente
    if offre.type == 'offre':
        # L'auteur de l'offre est le mentor
        Matching.objects.create(
            mentor=offre.utilisateurs,
            mentore_id=utilisateur_id,
            statut='en_attente'
        )
    else:
        # L'auteur de la demande est le mentoré
        Matching.objects.create(
            mentor_id=utilisateur_id,
            mentore=offre.utilisateurs,
            statut='en_attente'
        )

    return redirect('liste_offres')


def mes_offres(request):
    # Récupérer l'utilisateur connecté
    utilisateur_id = request.session.get('user_id')
    if not utilisateur_id:
        return redirect('login')

    # Récupérer toutes les offres de l'utilisateur connecté
    offres = OffresMentorat.objects.filter(
        utilisateurs_id=utilisateur_id
    ).order_by('-date_publication')

    return render(request, 'offres/mes_offres.html', {
        'offres': offres,
    })


def changer_statut(request, offre_id):
    # Activer ou désactiver une offre
    utilisateur_id = request.session.get('user_id')
    if not utilisateur_id:
        return redirect('login')

    offre = get_object_or_404(OffresMentorat, id=offre_id, utilisateurs_id=utilisateur_id)

    # Basculer le statut
    if offre.statut == 'active':
        offre.statut = 'inactive'
    else:
        offre.statut = 'active'

    offre.save()
    return redirect('mes_offres')

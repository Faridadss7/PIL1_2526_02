from django.shortcuts import render, get_object_or_404, redirect
from .models import Utilisateurs, PointsFaibles, PointsForts, Disponibilites, Matching, OffresMentorat, Conversations


# Afficher le formulaire de recherche
def recherche_mentor(request):
    return render(request, 'matching/recherche.html')


# Calculer le matching
def calculer_matching(request):
    utilisateur_id = request.session.get('utilisateur_id')
    utilisateur = get_object_or_404(Utilisateurs, id=utilisateur_id)

    # Récupérer les points faibles de l'utilisateur
    points_faibles = PointsFaibles.objects.filter(
        utilisateurs=utilisateur
    ).values_list('competences_id', flat=True)

    # Chercher les mentors dont les points forts correspondent
    mentors_potentiels = Utilisateurs.objects.filter(
        pointsforts__competences_id__in=points_faibles
    ).exclude(id=utilisateur_id).distinct()

    resultats = []

    for mentor in mentors_potentiels:
        # 1. Compétences en commun (50%)
        points_forts_mentor = PointsForts.objects.filter(
            utilisateurs=mentor
        ).values_list('competences_id', flat=True)
        communs = set(points_faibles) & set(points_forts_mentor)
        score_competences = (len(communs) / len(points_faibles)) * 50 if points_faibles else 0

        # 2. Disponibilités communes (30%)
        dispo_utilisateur = Disponibilites.objects.filter(
            utilisateur=utilisateur
        ).values_list('jour', flat=True)
        dispo_mentor = Disponibilites.objects.filter(
            utilisateur=mentor
        ).values_list('jour', flat=True)
        dispo_communes = set(dispo_utilisateur) & set(dispo_mentor)
        score_dispo = (len(dispo_communes) / len(dispo_utilisateur)) * 30 if dispo_utilisateur else 0

        # 3. Proximité filière (20%)
        score_filiere = 20 if mentor.filiere == utilisateur.filiere else 0

        # Score total
        score_total = score_competences + score_dispo + score_filiere

        resultats.append({
            'mentor': mentor,
            'score': round(score_total, 2),
            'communs': communs,
            'dispo_communes': dispo_communes,
        })

    # Trier par score décroissant
    resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)

    return render(request, 'matching/resultats.html', {'resultats': resultats})


# Détail d'un mentor
def detail_mentor(request, mentor_id):
    mentor = get_object_or_404(Utilisateurs, id=mentor_id)
    points_forts = PointsForts.objects.filter(utilisateurs=mentor)
    disponibilites = Disponibilites.objects.filter(utilisateur=mentor)
    return render(request, 'matching/detail_mentor.html', {
        'mentor': mentor,
        'points_forts': points_forts,
        'disponibilites': disponibilites,
    })


# Publier une offre
def publier_offre(request):
    if request.method == 'POST':
        utilisateur_id = request.session.get('utilisateur_id')
        utilisateur = get_object_or_404(Utilisateurs, id=utilisateur_id)
        OffresMentorat.objects.create(
            utilisateurs=utilisateur,
            type=request.POST.get('type'),
            competences_id=request.POST.get('competence_id'),
            format=request.POST.get('format'),
            description=request.POST.get('description'),
        )
        return redirect('recherche')
    return render(request, 'matching/publier_offre.html')


# Répondre à une offre
def repondre_offre(request, offre_id):
    utilisateur_id = request.session.get('utilisateur_id')
    offre = get_object_or_404(OffresMentorat, id=offre_id)
    Matching.objects.create(
        mentor=offre.utilisateurs,
        mentore_id=utilisateur_id,
        statut='en_attente'
    )
    return redirect('recherche')


# Accepter un matching
def accepter_matching(request, matching_id):
    matching = get_object_or_404(Matching, id=matching_id)
    matching.statut = 'accepte'
    matching.save()
    Conversations.objects.create(matching=matching)
    return redirect('recherche')


# Refuser un matching
def refuser_matching(request, matching_id):
    matching = get_object_or_404(Matching, id=matching_id)
    matching.statut = 'refuse'
    matching.save()
    return redirect('recherche')

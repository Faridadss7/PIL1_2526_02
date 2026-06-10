from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q, Count
from app.auth.accounts.db_guard import require_metier_schema
from app.auth.accounts.sync_utilisateur import ensure_utilisateur
from app.matching.models import (
    OffresMentorat, Competences, Matching, Utilisateurs,
    PointsForts, Disponibilites, Conversations
)


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
    jour_dispo = request.GET.get('jour_dispo', '')
    format_recherche = request.GET.get('format', '')
    offres = OffresMentorat.objects.filter(statut='active').select_related(
        'competences', 'utilisateurs'
    )
    if matiere:
        offres = offres.filter(competences__nom__icontains=matiere)
    if format_recherche:
        offres = offres.filter(format=format_recherche)
    if jour_dispo:
        offre_ids = OffresMentorat.objects.filter(
            statut='active'
        ).values_list('utilisateurs_id', flat=True)
        utilisateurs_with_dispo = Disponibilites.objects.filter(
            utilisateur_id__in=offre_ids,
            jour=jour_dispo
        ).values_list('utilisateur_id', flat=True)
        offres = offres.filter(utilisateurs_id__in=utilisateurs_with_dispo)
    offres = offres.order_by('-date_publication')
    
    # Calculate notifications
    nb_matchings_en_attente = Matching.objects.filter(
        mentor_id=request.user.id,
        statut='en_attente'
    ).count()
    from app.messagerie.utils import messages_utilisateur
    msgs = messages_utilisateur(request.user.id)
    nb_non_lus = msgs.filter(lu=False).exclude(expediteur_id=request.user.id).count()
    nb_notifications = nb_matchings_en_attente + nb_non_lus
    
    return render(request, 'offres/Offres&Demandes.html', {
        'offres': offres,
        'competences': Competences.objects.all(),
        'user': request.user,
        'matiere': matiere,
        'jour_dispo': jour_dispo,
        'format_recherche': format_recherche,
        'nb_notifications': nb_notifications,
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
        competence_ids = request.POST.getlist('competence_ids')
        type_offre = request.POST.get('type')
        format_offre = request.POST.get('format')
        jour_dispo = request.POST.get('jour_dispo', '')
        heure_debut = request.POST.get('heure_debut', '')
        heure_fin = request.POST.get('heure_fin', '')
        
        if not competence_ids or not type_offre or not format_offre:
            django_messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('offres_demandes')
        
        try:
            utilisateur = ensure_utilisateur(request.user)
            
            for comp_id in competence_ids:
                OffresMentorat.objects.create(
                    utilisateurs=utilisateur,
                    type=type_offre,
                    competences_id=comp_id,
                    format=format_offre,
                    description=request.POST.get('description', ''),
                    statut='active'
                )
            
            if jour_dispo and heure_debut and heure_fin:
                Disponibilites.objects.create(
                    utilisateur=utilisateur,
                    jour=jour_dispo,
                    heure_debut=heure_debut,
                    heure_fin=heure_fin
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
            matching = Matching.objects.create(
                mentor=offre.utilisateurs,
                mentore=utilisateur,
                statut='en_attente'
            )
        else:
            matching = Matching.objects.create(
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
    
    # Note: Cannot link matchings to offers without offre_id field in Matching model
    # Setting nb_reponses to 0 for all offers
    for offre in offres:
        offre.nb_reponses = 0
    
    # Calculate notifications
    nb_matchings_en_attente = Matching.objects.filter(
        mentor_id=request.user.id,
        statut='en_attente'
    ).count()
    from app.messagerie.utils import messages_utilisateur
    msgs = messages_utilisateur(request.user.id)
    nb_non_lus = msgs.filter(lu=False).exclude(expediteur_id=request.user.id).count()
    nb_notifications = nb_matchings_en_attente + nb_non_lus
    
    return render(request, 'offres/Offres&Demandes.html', {
        'offres': offres,
        'competences': Competences.objects.all(),
        'user': request.user,
        'mes_offres_vue': True,
        'nb_notifications': nb_notifications,
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


@login_required
def resultats_offre(request, offre_id):
    try:
        ensure_utilisateur(request.user)
    except Exception as e:
        django_messages.error(request, f"Profil non synchronisé : {e}")
        return redirect('profil')
    
    offre = get_object_or_404(OffresMentorat, id=offre_id, utilisateurs_id=request.user.id)
    
    # Note: Cannot link matchings to offers without offre_id field in Matching model
    # This feature is disabled until database schema is updated
    reponses = []
    
    # Calculate notifications
    nb_matchings_en_attente = Matching.objects.filter(
        mentor_id=request.user.id,
        statut='en_attente'
    ).count()
    from app.messagerie.utils import messages_utilisateur
    msgs = messages_utilisateur(request.user.id)
    nb_non_lus = msgs.filter(lu=False).exclude(expediteur_id=request.user.id).count()
    nb_notifications = nb_matchings_en_attente + nb_non_lus
    
    return render(request, 'offres/resultats_offre.html', {
        'offre': offre,
        'reponses': reponses,
        'user': request.user,
        'nb_notifications': nb_notifications,
    })


@login_required
def accepter_reponse(request, matching_id):
    try:
        matching = get_object_or_404(Matching, id=matching_id)
        
        # Check if user is the mentor
        if matching.mentor_id != request.user.id:
            django_messages.error(request, "Accès non autorisé.")
            return redirect('mes_matchings')
        
        matching.statut = 'accepte'
        matching.save()
        
        if not Conversations.objects.filter(matching=matching).exists():
            Conversations.objects.create(matching=matching)
        
        django_messages.success(request, "Réponse acceptée ! Une conversation a été créée.")
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
    
    return redirect('mes_matchings')


@login_required
def refuser_reponse(request, matching_id):
    try:
        matching = get_object_or_404(Matching, id=matching_id)
        
        # Check if user is the mentor
        if matching.mentor_id != request.user.id:
            django_messages.error(request, "Accès non autorisé.")
            return redirect('mes_matchings')
        
        matching.statut = 'refuse'
        matching.save()
        
        django_messages.info(request, "Réponse refusée.")
    except Exception as e:
        django_messages.error(request, f"Erreur : {str(e)}")
    
    return redirect('mes_matchings')

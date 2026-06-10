from django.urls import path

from app.matching import views as matching_views
from app.messagerie import views as messagerie_views
from app.offres import views as offres_views

from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('inscription/confirmation/', views.inscription_confirmation, name='inscription_confirmation'),
    path('renvoyer-activation/', views.renvoyer_activation, name='renvoyer_activation'),
    path('confirmer-email/<uidb64>/<token>/', views.confirmer_email, name='confirmer_email'),
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sessions/', views.sessions, name='sessions'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.vue_parametres, name='settings'),
    # Offres (actions avant la liste)
    path('offres/publier/', offres_views.publier_offre, name='publier_offre'),
    path('offres/repondre/<int:offre_id>/', offres_views.repondre_offre, name='repondre_offre'),
    path('offres/mes-offres/', offres_views.mes_offres, name='mes_offres'),
    path('offres/statut/<int:offre_id>/', offres_views.changer_statut, name='changer_statut'),
    path('offres/', views.offres_demandes, name='offres_demandes'),
    # Matching
    path('matchings/calculer/', matching_views.calculer_matching, name='calculer_matching'),
    path('matchings/contacter/<int:utilisateur_id>/', matching_views.contacter_direct, name='contacter_direct'),
    path('matchings/mes-matchings/', matching_views.mes_matchings, name='mes_matchings'),
    path('matchings/mentor/<int:mentor_id>/', matching_views.detail_mentor, name='detail_mentor'),
    path('matchings/accepter/<int:matching_id>/', matching_views.accepter_matching, name='accepter'),
    path('matchings/refuser/<int:matching_id>/', matching_views.refuser_matching, name='refuser'),
    path('matchings/', views.matchings, name='matchings'),
    # Messagerie (actions avant la liste)
    path('messages/chat/<int:conversation_id>/', messagerie_views.chat, name='chat'),
    path('messages/envoyer/<int:conversation_id>/', messagerie_views.envoyer_message, name='envoyer_message'),
    path('messages/marquer/<int:message_id>/', messagerie_views.marquer_lu, name='marquer_lu'),
    path('messages/marquer-tout/', messagerie_views.marquer_tout_lu, name='marquer_tout_lu'),
    path('messages/', views.vue_messagerie, name='messages'),
]

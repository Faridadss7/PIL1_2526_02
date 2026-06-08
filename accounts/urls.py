from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('', views.accueil, name='accueil'),
    path('offres/', views.offres_demandes, name='offres_demandes'),
    path('matchings/', views.matchings, name='matchings'),
    path('messages/', views.vue_messagerie, name='messages'),
    path('sessions/', views.sessions, name='sessions'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.vue_parametres, name='settings'),
    path('dashboard/', views.dashboard, name='dashboard'),   ]
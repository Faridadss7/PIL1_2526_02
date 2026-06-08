from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_offres, name='liste_offres'),
    path('publier/', views.publier_offre, name='publier_offre'),
    path('<int:offre_id>/', views.detail_offre, name='detail_offre'),
    path('repondre/<int:offre_id>/', views.repondre_offre, name='repondre_offre'),
    path('mes-offres/', views.mes_offres, name='mes_offres'),
    path('statut/<int:offre_id>/', views.changer_statut, name='changer_statut'),
]

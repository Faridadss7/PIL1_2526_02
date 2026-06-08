from django.urls import path
from . import views

urlpatterns = [
    path('recherche/', views.recherche_mentor, name='recherche_mentor'),
    path('matching/', views.calculer_matching, name='calculer_matching'),
    path('mentor/<int:mentor_id>/', views.detail_mentor, name='detail_mentor'),
    path('publier/', views.publier_offre, name='publier_offre'),
    path('repondre/<int:offre_id>/', views.repondre_offre, name='repondre_offre'),
    path('accepter/<int:matching_id>/', views.accepter_matching, name='accepter_matching'),
    path('refuser/<int:matching_id>/', views.refuser_matching, name='refuser_matching'),
]
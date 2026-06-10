from django.urls import path
from . import views

urlpatterns = [
    # Note: resultats_offre, accepter_reponse, refuser_reponse disabled - need offre_id in Matching model
    # path('resultats/<int:offre_id>/', views.resultats_offre, name='resultats_offre'),
    # path('accepter-reponse/<int:matching_id>/', views.accepter_reponse, name='accepter_reponse'),
    # path('refuser-reponse/<int:matching_id>/', views.refuser_reponse, name='refuser_reponse'),
]

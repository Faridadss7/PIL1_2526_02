from django.urls import path
from . import views

urlpatterns = [
    path('contacter/<int:utilisateur_id>/', views.contacter_direct, name='contacter_direct'),
    path('mes-matchings/', views.mes_matchings, name='mes_matchings'),
]

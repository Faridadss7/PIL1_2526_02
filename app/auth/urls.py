from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
    path('add_competence/', views.add_competence, name='add_competence'),
    path('remove_competence/<str:type_c>/<int:comp_id>/', views.remove_competence, name='remove_competence'),
    path('add_disponibilite/', views.add_disponibilite, name='add_disponibilite'),
    path('remove_disponibilite/<int:dispo_id>/', views.remove_disponibilite, name='remove_disponibilite'),
    path('add_offre/', views.add_offre, name='add_offre'),
]
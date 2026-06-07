from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_conversations, name='liste_conversations'),
    path('chat/<int:conversation_id>/', views.chat, name='chat'),
    path('envoyer/<int:conversation_id>/', views.envoyer_message, name='envoyer_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('marquer/<int:message_id>/', views.marquer_lu, name='marquer_lu'),
]

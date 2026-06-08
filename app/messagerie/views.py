from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversations, Messages


def liste_conversations(request):
    # Récupérer toutes les conversations de l'utilisateur connecté via les messages envoyés ou reçus
    utilisateur_id=request.session.get('user_id')
    if not utiisateur_id:
        return redirect('login')
                                       
    conversations = Conversations.objects.filter(
        messages__expediteur_id=utilisateur_id
    ).distinct()

    return render(request, 'messagerie/conversations.html', {
        'conversations': conversations
    })

def chat(request, conversation_id):
    
    utilisateur_id=request.session.get('user_id')
    if not utiisateur_id:
        return redirect('login')
    # Récupérer la conversation
    conversation = get_object_or_404(Conversations, id=conversation_id)

    # Récupérer tous les messages de cette conversation
    messages = Messages.objects.filter(
        conversations_id=conversation_id
    ).order_by('date_envoi')

    # Marquer les messages reçus comme lus
    Messages.objects.filter(
        conversations_id=conversation_id,
        lu=False
    ).exclude(
        expediteur_id=utilisateur_id
    ).update(lu=True)

    return render(request, 'messagerie/chat.html', {
        'conversation': conversation,
        'messages': messages
    })

def envoyer_message(request, conversation_id):
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            # Enregistrer le message dans la base de données 
            Messages.objects.create(
                conversations_id=conversation_id,
                expediteur_id=request.session.get('user_id')
                contenu=contenu,
                lu=False
            )
    return redirect('chat', conversation_id=conversation_id)


def notifications(request):
    # Récupérer tous les messages non lus de l'utilisateur connecté
    messages_non_lus = Messages.objects.filter(
        lu=False
    ).exclude(
        expediteur_id=request.session.get('user_id')
    ).order_by('-date_envoi')

    return render(request, 'messagerie/notifications.html', {
        'messages_non_lus': messages_non_lus
    })


def marquer_lu(request, message_id):
    # Marquer un message comme lu
    message = get_object_or_404(Messages, id=message_id)
    message.lu = True
    message.save()
    return redirect('liste_conversations')

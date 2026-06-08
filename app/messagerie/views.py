from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversations, Messages


@login_required
def liste_conversations(request):
    # Récupérer toutes les conversations de l'utilisateur connecté
    # via les messages envoyés ou reçus
    conversations = Conversations.objects.filter(
        messages__expediteur_id=request.user.id
    ).distinct()

    return render(request, 'messagerie/conversations.html', {
        'conversations': conversations
    })


@login_required
def chat(request, conversation_id):
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
        expediteur_id=request.user.id
    ).update(lu=True)

    return render(request, 'messagerie/chat.html', {
        'conversation': conversation,
        'messages': messages
    })


@login_required
def envoyer_message(request, conversation_id):
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            # Enregistrer le message dans la base de données
            Messages.objects.create(
                conversations_id=conversation_id,
                expediteur_id=request.user.id,
                contenu=contenu,
                lu=False
            )
    return redirect('chat', conversation_id=conversation_id)


@login_required
def notifications(request):
    # Récupérer tous les messages non lus de l'utilisateur connecté
    messages_non_lus = Messages.objects.filter(
        lu=False
    ).exclude(
        expediteur_id=request.user.id
    ).order_by('-date_envoi')

    return render(request, 'messagerie/notifications.html', {
        'messages_non_lus': messages_non_lus
    })


@login_required
def marquer_lu(request, message_id):
    # Marquer un message comme lu
    message = get_object_or_404(Messages, id=message_id)
    message.lu = True
    message.save()
    return redirect('liste_conversations')

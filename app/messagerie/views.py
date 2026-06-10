from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from app.auth.accounts.db_guard import require_metier_schema
from app.auth.accounts.sync_utilisateur import ensure_utilisateur
from app.matching.models import Conversations, Messages, Matching
from .utils import conversations_utilisateur, est_participant, messages_utilisateur


def _ensure_messagerie_user(request):
    if not require_metier_schema(request):
        return False
    try:
        ensure_utilisateur(request.user)
    except Exception as e:
        django_messages.error(request, f"Profil non synchronisé : {e}")
        return False
    return True


@login_required
def liste_conversations(request):
    if not _ensure_messagerie_user(request):
        return render(request, 'messagerie/messages.html', {
            'conversations': [],
            'user': request.user,
        })
    conversations = conversations_utilisateur(request.user.id)
    return render(request, 'messagerie/messages.html', {
        'conversations': conversations,
        'user': request.user,
    })


@login_required
def chat(request, conversation_id):
    if not _ensure_messagerie_user(request):
        return redirect('messages')
    conversation = get_object_or_404(
        Conversations.objects.select_related('matching'),
        id=conversation_id,
    )
    if not est_participant(conversation, request.user.id):
        django_messages.error(request, "Vous n'êtes pas participant de cette conversation.")
        return redirect('messages')

    messages_list = Messages.objects.filter(
        conversations_id=conversation_id
    ).select_related('expediteur').order_by('date_envoi')

    Messages.objects.filter(
        conversations_id=conversation_id,
        lu=False
    ).exclude(expediteur_id=request.user.id).update(lu=True)

    return render(request, 'messagerie/messages.html', {
        'conversation': conversation,
        'messages_list': messages_list,
        'conversations': conversations_utilisateur(request.user.id),
        'conversation_active': True,
        'user': request.user,
    })


@login_required
def envoyer_message(request, conversation_id):
    conversation = get_object_or_404(
        Conversations.objects.select_related('matching'),
        id=conversation_id,
    )
    if not est_participant(conversation, request.user.id):
        django_messages.error(request, "Vous n'êtes pas participant de cette conversation.")
        return redirect('messages')

    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        if contenu:
            ensure_utilisateur(request.user)
            Messages.objects.create(
                conversations_id=conversation_id,
                expediteur_id=request.user.id,
                contenu=contenu,
                lu=False,
            )
    return redirect('chat', conversation_id=conversation_id)


@login_required
def notifications(request):
    if not _ensure_messagerie_user(request):
        return render(request, 'messagerie/notifications.html', {
            'messages_non_lus': [],
            'matchings_en_attente': [],
            'user': request.user,
        })
    messages_non_lus = messages_utilisateur(request.user.id).filter(
        lu=False,
    ).exclude(
        expediteur_id=request.user.id,
    ).select_related('expediteur', 'conversations').order_by('-date_envoi')
    
    matchings_en_attente = Matching.objects.filter(
        mentor_id=request.user.id,
        statut='en_attente'
    ).select_related('mentore').order_by('-date_matching')
    
    return render(request, 'messagerie/notifications.html', {
        'messages_non_lus': messages_non_lus,
        'matchings_en_attente': matchings_en_attente,
        'user': request.user,
    })


@login_required
def marquer_tout_lu(request):
    if request.method == 'POST':
        messages_utilisateur(request.user.id).filter(
            lu=False,
        ).exclude(
            expediteur_id=request.user.id,
        ).update(lu=True)
        django_messages.success(request, "Toutes les notifications ont été marquées comme lues.")
    return redirect('notifications')


@login_required
def marquer_lu(request, message_id):
    message = get_object_or_404(
        Messages.objects.select_related('conversations', 'conversations__matching'),
        id=message_id,
    )
    if not est_participant(message.conversations, request.user.id):
        django_messages.error(request, "Accès non autorisé à ce message.")
        return redirect('messages')
    message.lu = True
    message.save()
    return redirect('messages')

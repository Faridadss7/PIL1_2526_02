from django.db.models import Q, OuterRef, Subquery
from app.matching.models import Conversations, Messages


def conversations_utilisateur(user_id):
    """Conversations où l'utilisateur est mentor ou mentoré via le matching lié."""
    dernier_message = Messages.objects.filter(
        conversations_id=OuterRef('pk'),
    ).order_by('-date_envoi')

    return Conversations.objects.filter(
        matching__isnull=False,
    ).filter(
        Q(matching__mentor_id=user_id) | Q(matching__mentore_id=user_id)
    ).select_related(
        'matching', 'matching__mentor', 'matching__mentore',
    ).annotate(
        dernier_contenu=Subquery(dernier_message.values('contenu')[:1]),
        dernier_date=Subquery(dernier_message.values('date_envoi')[:1]),
    ).order_by('-dernier_date', '-date_creation')


def conversation_ids_utilisateur(user_id):
    return conversations_utilisateur(user_id).values_list('id', flat=True)


def est_participant(conversation, user_id):
    matching = conversation.matching
    if not matching:
        return False
    return matching.mentor_id == user_id or matching.mentore_id == user_id


def messages_utilisateur(user_id):
    """Messages appartenant aux conversations de l'utilisateur."""
    conv_ids = list(conversation_ids_utilisateur(user_id))
    if not conv_ids:
        return Messages.objects.none()
    return Messages.objects.filter(conversations_id__in=conv_ids)

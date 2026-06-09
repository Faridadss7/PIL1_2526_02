from django.contrib import messages as django_messages
from django.db.utils import ProgrammingError

from .db_setup import metier_schema_ready

SETUP_MESSAGE = (
    "La base métier n'est pas initialisée. "
    "Exécutez dans un terminal : py manage.py setup_metier"
)


def require_metier_schema(request):
    """Retourne False si le schema métier manque (message utilisateur posé)."""
    if metier_schema_ready():
        return True
    django_messages.error(request, SETUP_MESSAGE)
    return False


def safe_metier_call(request, callback, fallback_context):
    """
    Exécute callback() ; en cas de tables absentes, affiche un message
    et retourne le contexte de repli sans planter.
    """
    if not metier_schema_ready():
        django_messages.error(request, SETUP_MESSAGE)
        return fallback_context
    try:
        return callback()
    except ProgrammingError:
        django_messages.error(request, SETUP_MESSAGE)
        return fallback_context

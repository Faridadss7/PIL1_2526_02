from pathlib import Path

from django.conf import settings
from django.db import connection


METIER_TABLES = (
    'utilisateurs',
    'competences',
    'points_forts',
    'points_faibles',
    'disponibilites',
    'offres_mentorat',
    'matching',
    'conversations',
    'messages',
)


def metier_schema_ready():
    """Vérifie que les tables métier du schema.sql existent."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = ANY(%s)
            """,
            [list(METIER_TABLES)],
        )
        return cursor.fetchone()[0] == len(METIER_TABLES)


def execute_schema_sql():
    """Exécute database/schema.sql (création tables + compétences)."""
    schema_path = Path(settings.BASE_DIR) / 'database' / 'schema.sql'
    sql = schema_path.read_text(encoding='utf-8')

    statements = []
    buffer = []
    for line in sql.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('--'):
            continue
        buffer.append(line)
        if stripped.endswith(';'):
            statements.append('\n'.join(buffer))
            buffer = []

    with connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)


def sync_all_django_users():
    from django.contrib.auth import get_user_model

    from .sync_utilisateur import ensure_utilisateur

    for user in get_user_model().objects.all():
        ensure_utilisateur(user)

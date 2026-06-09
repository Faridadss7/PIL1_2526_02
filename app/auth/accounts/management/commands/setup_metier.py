from django.core.management.base import BaseCommand

from app.auth.accounts.db_setup import (
    execute_schema_sql,
    metier_schema_ready,
    sync_all_django_users,
)


class Command(BaseCommand):
    help = (
        "Crée les tables métier (utilisateurs, compétences, offres, messages…) "
        "et synchronise les comptes Django existants."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Réexécute schema.sql (supprime et recrée les tables métier).',
        )

    def handle(self, *args, **options):
        if metier_schema_ready() and not options['force']:
            self.stdout.write(self.style.WARNING(
                'Les tables métier existent déjà. Utilisez --force pour tout recréer.'
            ))
        else:
            self.stdout.write('Chargement de database/schema.sql…')
            execute_schema_sql()
            self.stdout.write(self.style.SUCCESS('Tables métier créées.'))

        self.stdout.write('Synchronisation des utilisateurs Django vers utilisateurs...')
        sync_all_django_users()
        self.stdout.write(self.style.SUCCESS('Terminé. Relancez le serveur et reconnectez-vous.'))

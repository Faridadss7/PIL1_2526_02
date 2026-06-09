from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration pour corriger le conflit de table.
    Le modèle User n'utilise plus db_table='utilisateurs'.
    Django va utiliser 'accounts_user' automatiquement.
    """

    dependencies = [
        ('accounts', '0005_alter_user_bio_alter_user_filiere_alter_user_niveau_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table=None,  # None = Django utilise le nom par défaut 'accounts_user'
        ),
    ]

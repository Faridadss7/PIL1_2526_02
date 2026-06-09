from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_db_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='centre_interet',
            field=models.TextField(blank=True, null=True),
        ),
    ]

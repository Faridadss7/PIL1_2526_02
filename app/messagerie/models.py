from django.db import models


class Conversations(models.Model):
    matching_id = models.IntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'conversations'


class Messages(models.Model):
    conversations_id = models.IntegerField()
    expediteur_id = models.IntegerField()
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'messages'

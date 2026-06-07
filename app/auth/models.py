from django.db import models

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telephone = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=260)
    photo_profil = models.CharField(max_length=260, blank=True, null=True)
    filiere = models.CharField(max_length=150)
    niveau = models.CharField(max_length=10)
    bio = models.TextField(blank=True, null=True)
    centre_interet = models.TextField(db_column='Centre_interet', blank=True, null=True)  # Respect de la majuscule SQL
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'utilisateurs'
        managed = False

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Competence(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    niveau = models.CharField(max_length=10)

    class Meta:
        db_table = 'competences'
        managed = False


class PointsForts(models.Model):
    id = models.AutoField(primary_key=True)
    competences = models.ForeignKey(Competence, on_delete=models.CASCADE, db_column='competences_id')
    utilisateurs = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='utilisateurs_id')

    class Meta:
        db_table = 'points_forts'
        managed = False


class PointsFaibles(models.Model):
    id = models.AutoField(primary_key=True)
    competences = models.ForeignKey(Competence, on_delete=models.CASCADE, db_column='competences_id')
    utilisateurs = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='utilisateurs_id')

    class Meta:
        db_table = 'points_faibles'
        managed = False


class Disponibilite(models.Model):
    id = models.AutoField(primary_key=True)
    jour = models.CharField(max_length=20, blank=True, null=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='utilisateur_id')
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'disponibilites'
        managed = False


class OffreMentorat(models.Model):
    id = models.AutoField(primary_key=True)
    utilisateurs = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='utilisateurs_id')
    type = models.CharField(max_length=20)  # 'offre' ou 'demande' dans le CHECK SQL
    competences = models.ForeignKey(Competence, on_delete=models.CASCADE, db_column='competences_id')
    format = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, default='active')
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'offres_mentorat'
        managed = False


class Matching(models.Model):
    id = models.AutoField(primary_key=True)
    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='mentor_id', related_name='matching_mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='mentore_id', related_name='matching_mentore')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    statut = models.CharField(max_length=20, default='en_attente')
    date_matching = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'matching'
        managed = False


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    matching = models.ForeignKey(Matching, on_delete=models.SET_NULL, db_column='matching_id', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'
        managed = False


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversations = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_column='conversations_id')
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='expediteur_id')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        db_table = 'messages'
        managed = False
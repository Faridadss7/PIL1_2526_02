from django.db import models


class Utilisateurs(models.Model):
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
    centre_interet = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'utilisateurs'

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Competences(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200, unique=True)
    niveau = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'competences'

    def __str__(self):
        return self.nom


class PointsForts(models.Model):
    id = models.AutoField(primary_key=True)
    competences = models.ForeignKey(
        Competences, on_delete=models.CASCADE, db_column='competences_id',
        related_name='points_forts'
    )
    utilisateurs = models.ForeignKey(
        Utilisateurs, on_delete=models.CASCADE, db_column='utilisateurs_id',
        related_name='points_forts'
    )

    class Meta:
        managed = False
        db_table = 'points_forts'

    def __str__(self):
        return f"{self.utilisateurs} - {self.competences}"


class PointsFaibles(models.Model):
    id = models.AutoField(primary_key=True)
    competences = models.ForeignKey(
        Competences, on_delete=models.CASCADE, db_column='competences_id',
        related_name='points_faibles'
    )
    utilisateurs = models.ForeignKey(
        Utilisateurs, on_delete=models.CASCADE, db_column='utilisateurs_id',
        related_name='points_faibles'
    )

    class Meta:
        managed = False
        db_table = 'points_faibles'

    def __str__(self):
        return f"{self.utilisateurs} - {self.competences}"


class Disponibilites(models.Model):
    id = models.AutoField(primary_key=True)
    jour = models.CharField(max_length=20)
    utilisateur = models.ForeignKey(
        Utilisateurs, on_delete=models.CASCADE, db_column='utilisateur_id',
        related_name='disponibilites'
    )
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        managed = False
        db_table = 'disponibilites'

    def __str__(self):
        return f"{self.utilisateur} - {self.jour}"


class OffresMentorat(models.Model):
    id = models.AutoField(primary_key=True)
    utilisateurs = models.ForeignKey(
        Utilisateurs, on_delete=models.CASCADE, db_column='utilisateurs_id',
        related_name='offres'
    )
    type = models.CharField(max_length=20)
    competences = models.ForeignKey(
        Competences, on_delete=models.CASCADE, db_column='competences_id',
        related_name='offres'
    )
    format = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, default='active')
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'offres_mentorat'

    def __str__(self):
        return f"{self.type} - {self.competences}"


class Matching(models.Model):
    id = models.AutoField(primary_key=True)
    mentor = models.ForeignKey(
        Utilisateurs, on_delete=models.CASCADE,
        db_column='mentor_id', related_name='matching_mentor'
    )
    mentore = models.ForeignKey(
        Utilisateurs, on_delete=models.CASCADE,
        db_column='mentore_id', related_name='matching_mentore'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    statut = models.CharField(max_length=20, default='en_attente')
    date_matching = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'matching'

    def __str__(self):
        return f"{self.mentor} → {self.mentore}"


class Conversations(models.Model):
    id = models.AutoField(primary_key=True)
    matching = models.ForeignKey(
        Matching, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='matching_id', related_name='conversations'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'conversations'

    def __str__(self):
        return f"Conversation {self.id}"


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    conversations = models.ForeignKey(
        Conversations, on_delete=models.CASCADE,
        db_column='conversations_id', related_name='messages'
    )
    expediteur = models.ForeignKey(
        Utilisateurs, on_delete=models.PROTECT,
        db_column='expediteur_id', related_name='messages_envoyes'
    )
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'messages'

    def __str__(self):
        return f"Message {self.id} de {self.expediteur}"

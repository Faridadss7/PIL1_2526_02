from django.db import models


class Utilisateurs(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telephone = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=260)
    photo_profil = models.CharField(max_length=260, blank=True, null=True)
    filiere = models.CharField(max_length=150)
    niveau = models.CharField(max_length=10)
    bio = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'utilisateurs'

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Competences(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    niveau = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'competences'

    def __str__(self):
        return self.nom


class OffresMentorat(models.Model):
    utilisateurs = models.ForeignKey(
        Utilisateurs,
        on_delete=models.CASCADE,
        db_column='utilisateurs_id'
    )
    type = models.CharField(max_length=20)
    competences = models.ForeignKey(
        Competences,
        on_delete=models.CASCADE,
        db_column='competences_id'
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
    mentor = models.ForeignKey(
        Utilisateurs,
        on_delete=models.CASCADE,
        db_column='mentor_id',
        related_name='offres_matching_mentor'
    )
    mentore = models.ForeignKey(
        Utilisateurs,
        on_delete=models.CASCADE,
        db_column='mentore_id',
        related_name='offres_matching_mentore'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    statut = models.CharField(max_length=20, default='en_attente')
    date_matching = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'matching'

    def __str__(self):
        return f"{self.mentor} → {self.mentore}"

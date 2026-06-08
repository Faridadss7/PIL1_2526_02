from django.db import models

class Utilisateur(models.Model):
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

class Disponibilite(models.Model):
    jour = models.CharField(max_length=20)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        managed = False
        db_table = 'disponibilites'

class Competence(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    niveau = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'competences'

class PointFort(models.Model):
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'points_forts'

class PointFaible(models.Model):
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'points_faibles'

class OffreMentorat(models.Model):
    TYPE_CHOICES = [('offre', 'Offre'), ('demande', 'Demande')]
    FORMAT_CHOICES = [('presentiel', 'Présentiel'), ('en_ligne', 'En ligne'), ('les_deux', 'Les deux')]
    STATUT_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'offres_mentorat'

class Matching(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='mentore')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_matching = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'matching'

class Conversation(models.Model):
    matching = models.ForeignKey(Matching, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'conversations'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'messages'

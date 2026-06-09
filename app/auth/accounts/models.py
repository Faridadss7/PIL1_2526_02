from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100, unique=True)
    niveau = models.CharField(max_length=10)
    bio = models.TextField(blank=True, null=True)
    filiere = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to='photos/',
        blank=True, null=True,
        db_column='photo_profil'
    )
    centre_interet = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    # Pas de db_table custom → Django utilise 'accounts_user'
    # Le schema.sql crée 'utilisateurs' (table séparée pour matching/messagerie)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nom=models.CharField(max_length=30, verbose_name="Nom")
    prenom=models.CharField(max_length=30, verbose_name="Prénom")
    telephone = models.CharField(max_length=20, unique=True)
    filiere = models.CharField(max_length=100, blank=True)
    niveau = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    competences = models.TextField(blank=True)
    lacunes = models.TextField(blank=True)
    disponibilites = models.TextField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']
   
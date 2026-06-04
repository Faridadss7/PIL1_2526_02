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
    centre_interet = models.TextField(blank=True, null=True, db_column='Centre_interet')
    date_inscription = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']
    class Meta:
        db_table = 'utilisateurs'

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
   
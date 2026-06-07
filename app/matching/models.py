from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.models import User
class Utilisateurs(AbstractUser)
   class Meta:
     db_table ='utilisateur'p,
   def __str__(self):
       return self.username
class PointsForts (models.Model):
   utilisateur = models.ForeignKey(Utilisateurs,on_delete=models.CASCADE)
   libelle = models.CharField(max_length=255)
   
   
   
   
   class Meta:
      
      
      
      
      
      
      
      
      db_table ='points_forts'
      
      
      
      
      
   def __str__(self):
      
    return f"{self.utilisateur.username} -{self.libelle}" 
class PointsFaibles(models.Model):
   Utilisateurs = models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,related_name='points_faibles')
   libelle=models.CharField(max_length=255)
   
   
   
   class Meta:
      db_table ='points_faibles'





   def __str__(self):
      return f"{self.utilisateur.username} - {self.libelle}"
   
   
class Disponibilites(models.Model):       
   utilisateur = models.ForeignKey(User,on_delete=models.CASCADE)
   jour = models.CharField(max_length=20) 
   heure_debut = models.TimeField() 
   heure_fin = models.TimeField()
   
   
   class Meta:
      db_table = 'disponibilites' 
      unique_together = ('utilisateur','jour')
      
   def __str__(self):
      return f"{self.utilisateur} - {self.jour}"
   
     
class OffresMentorat (models.Model):    
   mentor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='offres')
   titre = models.CharField(max_length=200)
   description = models.TextField()
   date_creation = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table ='offres_mentorat'
   
   
   def __str__(self):
      return self.titre
   
   
class Matching(models.Model):
   offre = models.ForeignKey(OffresMentorat,on_delete=models.CASCADE)    
   mentee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='matchings')  
   date_match = models.DateTimeField(auto_now_add=True)
   statut = models.CharField(max_length=20,default='en attente')
   
   
   class Meta:
      db_table = 'matching'
      unique_together = ('offre','mentee')
      
      def __str__(self):
         return f"{self.mentee} -{self.offre}"
      
      
      
      
      
   
   
      

      
       
      
   
   
   
   
   
   

  
  
    
   
   
   

   
   
   
   
   
   
      
         
         
      

      
      
      
   

      
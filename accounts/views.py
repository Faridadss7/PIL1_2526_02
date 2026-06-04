from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InscriptionForm
from django.contrib.auth import login, logout, authenticate
from .forms import InscriptionForm, ConnexionForm

# 1. Ta fonction inscription actuelle
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Compte créé avec succès pour {user.prenom} ! Connectez-vous.")
            return redirect('connexion') 
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profil')
    else:
        form = ConnexionForm()
        
    return render(request, 'accounts/connexion.html', {'form': form})

def deconnexion(request):
    logout(request) 
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')

def profil(request):
    return render(request, 'accounts/profil.html')
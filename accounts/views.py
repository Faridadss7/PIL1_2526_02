from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from .forms import InscriptionForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import os


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_messages.success(request, f"Compte créé avec succès pour {user.prenom} ! Connectez-vous.")
            return redirect('connexion')
        else:
            print(form.errors)
    else:
        form = InscriptionForm()
    return render(request, 'pages/register.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profil')
        else:
            print("Erreur : Email ou mot de passe incorrect")
            return render(request, 'pages/login.html', {'error': 'Identifiants invalides'})
    return render(request, 'pages/login.html')


def deconnexion(request):
    logout(request)
    django_messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')


def accueil(request):
    return render(request, 'index.html')


@login_required
def profil(request):
    user = request.user
    if request.method == 'POST':
        user.competences = request.POST.get('competences', '')
        user.lacunes = request.POST.get('lacunes', '')
        user.disponibilites = request.POST.get('disponibilites', '')
        user.bio = request.POST.get('bio', '')
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            from django.conf import settings as django_settings
            media_dir = os.path.join(django_settings.BASE_DIR, 'media', 'profils')
            os.makedirs(media_dir, exist_ok=True)
            with open(os.path.join(media_dir, photo.name), 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)
            user.photo = f'profils/{photo.name}'
        user.save()
        django_messages.success(request, "Profil mis à jour !")
        return redirect('profil')
    return render(request, 'pages/profile.html', {'user': user})


@login_required
def offres_demandes(request):
    return render(request, 'pages/Offres&Demandes.html')


@login_required
def matchings(request):
    return render(request, 'pages/matchings.html')


@login_required
def vue_messagerie(request):
    return render(request, 'pages/messages.html')


@login_required
def sessions(request):
    return render(request, 'pages/sessions.html')


@login_required
def notifications(request):
    return render(request, 'pages/notifications.html')


@login_required
def vue_parametres(request):
    return render(request, 'pages/settings.html')


@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')
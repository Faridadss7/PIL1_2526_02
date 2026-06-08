from django.shortcuts import render, redirect, get_object_or_404  # type: ignore[import]
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from .models import Utilisateur, Competence, PointsForts, PointsFaibles, Disponibilite, OffreMentorat
from .forms import RegisterForm, LoginForm, EditProfileForm
from datetime import datetime

def login_required_custom(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, "Veuillez vous connecter pour accéder à cette page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']

            if Utilisateur.objects.filter(email=email).exists():
                messages.error(request, 'Email déjà utilisé')
                return render(request, 'register.html', {'form': form})
            if Utilisateur.objects.filter(telephone=telephone).exists():
                messages.error(request, 'Téléphone déjà utilisé')
                return render(request, 'register.html', {'form': form})

            user = form.save(commit=False)
            user.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])
            user.save()
            messages.success(request, 'Inscription réussie, connectez-vous')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['mot_de_passe']
            try:
                user = Utilisateur.objects.get(email=email)
                if check_password(password, user.mot_de_passe):
                    request.session['user_id'] = user.id
                    return redirect('profile')
            except Utilisateur.DoesNotExist:
                pass
            messages.error(request, 'Email ou mot de passe incorrect')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

@login_required_custom
def profile(request):
    user = Utilisateur.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'points_forts': PointsForts.objects.filter(utilisateurs=user),
        'points_faibles': PointsFaibles.objects.filter(utilisateurs=user),
        'disponibilites': Disponibilite.objects.filter(utilisateur=user),
        'offres': OffreMentorat.objects.filter(utilisateurs=user),
    }
    return render(request, 'profile.html', context)

@login_required_custom
def edit_profile(request):
    user = Utilisateur.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form, 'user': user})

@login_required_custom
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        user = Utilisateur.objects.get(id=request.session['user_id'])
        photo = request.FILES['photo']
        
        # Extension valide                            
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif']
        import os
        ext = os.path.splitext(photo.name)[1].lower()
        if ext not in allowed_extensions:
            messages.error(request, 'Format non autorisé (png, jpg, jpeg, gif)')
            return redirect('edit_profile')

        fs = FileSystemStorage(location='static/uploads')
        filename = fs.save(f"user_{user.id}_{photo.name}", photo)
        
        user.photo_profil = f"/static/uploads/{filename}"
        user.save()
        messages.success(request, 'Photo de profil mise à jour')
    else:
        messages.error(request, 'Aucun fichier sélectionné ou méthode invalide')
    return redirect('edit_profile')

@login_required_custom
def add_competence(request):
    if request.method == 'POST':
        user = Utilisateur.objects.get(id=request.session['user_id'])
        nom_competence = request.POST['nom_competence']
        niveau = request.POST['niveau_competence']
        type_competence = request.POST['type'] # 'fort' ou 'faible'

        # Récupère ou crée la compétence globale 
        competence, created = Competence.objects.get_or_create(
            nom=nom_competence,
            defaults={'niveau': niveau}
        )

        if type_competence == 'fort':
            if not PointsForts.objects.filter(competences=competence, utilisateurs=user).exists():
                PointsForts.objects.create(competences=competence, utilisateurs=user)
        else:
            if not PointsFaibles.objects.filter(competences=competence, utilisateurs=user).exists():
                PointsFaibles.objects.create(competences=competence, utilisateurs=user)

        messages.success(request, 'Compétence ajoutée')
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

@login_required_custom
def remove_competence(request, type_c, comp_id):
    user = Utilisateur.objects.get(id=request.session['user_id'])
    if type_c == 'fort':
        PointsForts.objects.filter(competences_id=comp_id, utilisateurs=user).delete()
    elif type_c == 'faible':
        PointsFaibles.objects.filter(competences_id=comp_id, utilisateurs=user).delete()
    messages.info(request, 'Compétence retirée')
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

@login_required_custom
def add_disponibilite(request):
    if request.method == 'POST':
        user = Utilisateur.objects.get(id=request.session['user_id'])
        jour = request.POST['jour']
        try:
            heure_debut = datetime.strptime(request.POST['heure_debut'], '%H:%M').time()
            heure_fin = datetime.strptime(request.POST['heure_fin'], '%H:%M').time()
        except ValueError:
            messages.error(request, "Format d'heure invalide. Utilisez HH:MM")
            return redirect(request.META.get('HTTP_REFERER', 'profile'))

        Disponibilite.objects.create(
            jour=jour, heure_debut=heure_debut, heure_fin=heure_fin, utilisateur=user
        )
        messages.success(request, 'Disponibilité ajoutée')
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

@login_required_custom
def remove_disponibilite(request, dispo_id):
    user = Utilisateur.objects.get(id=request.session['user_id'])
    dispo = get_object_or_404(Disponibilite, id=dispo_id)
    if dispo.utilisateur == user:
        dispo.delete()
        messages.info(request, 'Disponibilité supprimée')
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

@login_required_custom
def add_offre(request):
    if request.method == 'POST':
        user = Utilisateur.objects.get(id=request.session['user_id'])
        type_offre = request.POST['type_offre'] # Correspond au champ 'type' attendu par le CHECK du SQL
        competence_id = request.POST['competence_id']
        format_ = request.POST['format']
        description = request.POST.get('description', '')

        competence = get_object_or_404(Competence, id=competence_id)

        OffreMentorat.objects.create(
            utilisateurs=user,
            type=type_offre,
            competences=competence,
            format=format_,
            description=description
        )
        messages.success(request, 'Annonce publiée')
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

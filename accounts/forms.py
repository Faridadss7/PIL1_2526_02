from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

FILIERES = [
    ('', 'Sélectionnez votre filière'),
    ('GL', 'Génie Logiciel'),
    ('IA', 'Intelligence Artificielle'),
    ('IM', 'Ingénierie Mathématique'),
    ('SI', 'Systèmes Informatiques'),
    ('SE&IoT', 'Systèmes Embarqués & IoT'),
]

NIVEAUX = [
    ('', 'Sélectionnez votre niveau'),
    ('L1', 'Licence 1'),
    ('L2', 'Licence 2'),
    ('L3', 'Licence 3'),
]

class InscriptionForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False  # ← facultatif
    )
    centre_interet = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False  # ← facultatif
    )
    password1 = forms.CharField(
        label='Mot de Passe',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmer le Mot de Passe',
        widget=forms.PasswordInput
    )
    filiere = forms.ChoiceField(choices=FILIERES, label='Filière')
    niveau = forms.ChoiceField(choices=NIVEAUX, label='Niveau')

    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'telephone', 'filiere', 'niveau', 'password1', 'password2', 'bio', 'centre_interet' ]
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Adresse Email',
            'telephone': 'Numéro de téléphone',
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ConnexionForm(AuthenticationForm):
    username = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
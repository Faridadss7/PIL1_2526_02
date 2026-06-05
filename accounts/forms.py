from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class InscriptionForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'telephone', 'filiere', 'niveau']

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


class ConnexionForm(forms.Form):
    email = forms.EmailField(label='Adresse e-mail')
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput
    ) 

class ConnexionForm(AuthenticationForm):
    # On personnalise juste les étiquettes pour que ce soit en français
    username = forms.EmailField(label="Adresse Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
from django import forms

# Choix type offre
TYPE_OFFRE_CHOICES = [
    ('offre', 'Je veux être mentor'),
    ('demande', 'Je cherche un mentor'),
]

# Liste des matières S1
MATIERES_S1 = [
    ('logique', 'Logique, arithmétique et applications'),
    ('analyse_et_applications', 'Analyse et applications'),
    ('algebre_lineaire', 'Algèbre linéaire et application'),
    ('analyse_combinatoire', 'Analyse combinatoire, calculs des probabilités et applications'),
    ('statistiques_inferentielles', 'Statistiques inférentielles et applications'),
    ('architecture', 'Architecture et topologie des réseaux informatiques'),
    ('utilisation_et_administration', 'Utilisation et administration sous Windows/Linux'),
    ('outils_de_base', 'Outils de base en informatique'),
    ('algorithmique', 'Algorithmique'),
    ('langage_c', 'Langage C'),
    ('deontologie', 'Déontologie et droit liés aux TIC'),
    ('teeo', 'TEEO'),
]

# Liste des matières S2
MATIERES_S2 = [
    ('administration_reseaux', 'Administration des réseaux sous Windows/Linux'),
    ('suites_et_series', 'Suites et séries numériques'),
    ('equations_differentielles', 'Equations différentielles et calcul intégral'),
    ('projet_integrateur', 'Projet intégrateur'),
    ('theorie_des_graphes', 'Théorie des graphes et applications'),
    ('recherche_operationnelle', 'Recherche opérationnelle et application'),
    ('developpement_web', 'Développement web'),
    ('infographie', 'Infographie'),
    ('theorie_bdd', 'Théorie des bases de données et algèbre relationnelle'),
    ('sgbd_sql', 'SGBD et langage SQL'),
    ('programmation_python', 'Programmation python'),
    ('anglais_technique', 'Anglais technique'),
]

# Liste complète des matières
MATIERE_CHOICES = [('', '---Choisissez une matière---')] + MATIERES_S1 + MATIERES_S2

FORMAT_CHOICES = [
    ('', '---Choisissez un format---'),
    ('presentiel', 'Présentiel'),
    ('en_ligne', 'En ligne'),
    ('les_deux', 'Les deux'),
]

JOUR_CHOICES = [
    ('', '---Choisissez un jour---'),
    ('lundi', 'Lundi'),
    ('mardi', 'Mardi'),
    ('mercredi', 'Mercredi'),
    ('jeudi', 'Jeudi'),
    ('vendredi', 'Vendredi'),
    ('samedi', 'Samedi'),
    ('dimanche', 'Dimanche'),
]

HEURE_CHOICES = [('', 'Choisir une heure')] + [
    (f"{h:02d}:00", f"{h:02d}:00") for h in range(8, 21)
]


class RechercheForm(forms.Form):
    matiere = forms.ChoiceField(
        choices=MATIERE_CHOICES,
        label='Matière',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        label='Format',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    jour = forms.ChoiceField(
        choices=JOUR_CHOICES,
        label='Jour',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    heure_debut = forms.ChoiceField(
        choices=HEURE_CHOICES,
        label='Heure de début',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    heure_fin = forms.ChoiceField(
        choices=HEURE_CHOICES,
        label='Heure de fin',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')

        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                raise forms.ValidationError(
                    "L'heure de fin doit être après l'heure de début."
                )
        return cleaned_data


class PublierOffreForm(forms.Form):
    type_offre = forms.ChoiceField(
        choices=TYPE_OFFRE_CHOICES,
        label='Type',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    matiere = forms.ChoiceField(
        choices=MATIERE_CHOICES,
        label='Matière',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        label='Format',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    jour = forms.ChoiceField(
        choices=JOUR_CHOICES,
        label='Jour',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    heure_debut = forms.ChoiceField(
        choices=HEURE_CHOICES,
        label='Heure de début',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    heure_fin = forms.ChoiceField(
        choices=HEURE_CHOICES,
        label='Heure de fin',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='Description (facultatif)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Décrivez votre offre ou demande en quelques mots...',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')

        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                raise forms.ValidationError(
                    "L'heure de fin doit être après l'heure de début."
                )
        return cleaned_data

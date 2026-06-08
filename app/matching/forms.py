from django import forms


SEMESTRE_CHOICES = [
    ('S1', 'Semestre 1'),
    ('S2', 'Semestre 2'),
]

MATIERES_S1 = [
    ('logique', 'Logique, arithmétique et applications'),
    ('analyse_et_applications', 'Analyse et applications'),
    ('algebre_linéaire_et_applications', 'Algèbre linéaire et application'),
    ('analyse_combinatoire', 'Analyse combinatoire ,calculs des probalités et applications'),
    ('Statistiques_inferentielles','Statitiques inférentielles et applications'),
    ('Architecture','Architecture et topologie des réseaux informatiques'),
    ('Utilisation_et_administration','Utilisation et administration sous Windows/Linux'),
    ('Outils_de_base_en_informatique','Outils de base en informatique'),
    ('Algorithmique','Algorithmique'),
    ('Langage_C','Langage_C'),
    ('Déontologie_et_droit_liés_aux_TIC','Déontologie et droit liés aux TIC'),
    ('TEEO','TEEO'),
]
MATIERES_S2 = [
    ('Administration_des_réseaux_sous_Windows/Linux','Administration des réseaux sous Windows/Linux'),
    ('Suites_et_séries_numériques','Suites et séries numériques'),
    ('Equations_différentielles_et_calcul_intégral','Equations différentielles et calcul intégral'),
    ('Projet_intégrateur','Projet intégrateur'),
    ('Théorie_des_graphes','Théorie des graphes et applications'),
    ('Recherche_opérationnelle','Recherche opérationnelle et application'),
    ('Développement_web','Développement web'),
    ('Infographie','Infographie'),
    ('Théorie_des_bases_de_données_et_algèbre_relationnelle','Théorie des bases de données et algèbre relationnelle'),
    ('SGBD_et_langage_SQL','SGBD et langage SQL'),
    ('Programmation_python','Programmation python'),
    ('Anglais_technique','Anglais technique'),
]

MATIERE_CHOICES = MATIERES_S1 + MATIERES_S2

TYPE_OFFRE_CHOICES = [
    ('Offre', 'Offre'),
    ('Demande', 'Demande'),
]

FORMAT_CHOICES = [
    ('Présentiel','Présentiel'),
    ('En_ligne','En ligne'),
]

JOUR_CHOICES = [
    ('Lundi','Lundi'),
    ('Mardi','Mardi'),
    ('Mercredi','Mercredi'),
    ('Jeudi','Jeudi'),
    ('Vendredi','Vendredi'),
    ('Samedi','Samedi'),
    ('Dimanche','Dimanche'),
]

HEURE_CHOICES = [('', 'Choisir une heure')] + [
    (f"{h:02d}:00", f"{h:02d}:00") for h in range(6, 23)
]

class RechercheForm(forms.Form):

    matiere = forms.ChoiceField(
        choices=MATIERE_CHOICES,
        label='Matière',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        label='Format',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    jour = forms.ChoiceField(
        choices=JOUR_CHOICES,
        label='Jour',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    heure_debut = forms.ChoiceField(
        choices=HEURE_CHOICES,
        label='Heure de début',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    heure_fin = forms.ChoiceField(
        choices=HEURE_CHOICES,
        label='Heure de fin',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        
        print("=== RechercheForm : validation ===")
        print(f" matiere : {cleaned_data.get('matiere')}")
        print(f" format : {cleaned_data.get('format')}")
        print(f" jour : {cleaned_data.get('jour')}")
        print(f" heure_debut: {heure_debut}")
        print(f" heure_fin : {heure_fin}")
        
        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                print(" ERREUR : heure_fin <= heure_debut")
                raise forms.ValidationError(
                    "L'heure de fin doit être après l'heure de début."
                )
        print(" Validation OK")
        return cleaned_data



class PublierOffreForm(forms.Form):

    type_offre = forms.ChoiceField(
        choices=TYPE_OFFRE_CHOICES,
        label='Type',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    matiere = forms.ChoiceField(
        choices=MATIERES_CHOICES,
        label='Matière',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        label='Format',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    jour = forms.ChoiceField(
        choices=JOURS_CHOICES,
        label='Jour',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    heure_debut = forms.ChoiceField(
        choices=HEURES_CHOICES,
        label='Heure de début',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    heure_fin = forms.ChoiceField(
        choices=HEURES_CHOICES,
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

        print("=== PublierOffreForm : validation ===")
        print(f"  type_offre : {cleaned_data.get('type_offre')}")
        print(f"  matiere    : {cleaned_data.get('matiere')}")
        print(f"  format     : {cleaned_data.get('format')}")
        print(f"  jour       : {cleaned_data.get('jour')}")
        print(f"  heure_debut: {heure_debut}")
        print(f"  heure_fin  : {heure_fin}")
        print(f"  description: {cleaned_data.get('description')}")

        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                print("  ERREUR : heure_fin <= heure_debut")
                raise forms.ValidationError(
                    "L'heure de fin doit être après l'heure de début."
                )

        print("  Validation OK")
        return cleaned_data
        
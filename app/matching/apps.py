from django.apps import AppConfig

class MatchingConfig(AppConfig):
    name = 'app.matching'









    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')

        print("=== RechercheForm : validation ===")
        print(f"  matiere    : {cleaned_data.get('matiere')}")
        print(f"  format     : {cleaned_data.get('format')}")
        print(f"  jour       : {cleaned_data.get('jour')}")
        print(f"  heure_debut: {heure_debut}")
        print(f"  heure_fin  : {heure_fin}")

        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                print("  ERREUR : heure_fin <= heure_debut")
                raise forms.ValidationError(
                    "L'heure de fin doit être après l'heure de début."
                )

        print("  Validation OK")
        return cleaned_data

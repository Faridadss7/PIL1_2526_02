from django.db import connection

from app.matching.models import Utilisateurs


def ensure_utilisateur(user):
    """
    Garantit qu'une ligne existe dans la table métier `utilisateurs`
    (même id que le User Django). Requis pour offres, matching, messages.
    """
    telephone = (user.telephone or '').strip()
    if not telephone:
        telephone = f'user-{user.id}'

    photo_profil = ''
    if user.photo:
        photo_profil = str(user.photo)

    utilisateur, _ = Utilisateurs.objects.update_or_create(
        id=user.id,
        defaults={
            'nom': user.nom or '',
            'prenom': user.prenom or '',
            'email': user.email,
            'telephone': telephone,
            'mot_de_passe': user.password or '',
            'filiere': user.filiere or '',
            'niveau': user.niveau or 'L1',
            'bio': user.bio or '',
            'centre_interet': user.centre_interet or '',
            'photo_profil': photo_profil,
        },
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('utilisateurs', 'id'), "
                "GREATEST((SELECT COALESCE(MAX(id), 1) FROM utilisateurs), %s))",
                [user.id],
            )
    except Exception:
        pass

    return utilisateur

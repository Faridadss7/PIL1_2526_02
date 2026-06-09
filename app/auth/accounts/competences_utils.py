import json

from app.matching.models import Competences, PointsFaibles, PointsForts


def competences_par_niveau():
    result = {}
    for comp in Competences.objects.all().order_by('nom'):
        result.setdefault(comp.niveau, []).append(comp.nom)
    return result


def competences_par_niveau_json():
    return json.dumps(competences_par_niveau(), ensure_ascii=False)


def sync_points_forts(user_id, noms_competences):
    PointsForts.objects.filter(utilisateurs_id=user_id).delete()
    for nom_comp in noms_competences:
        comp = Competences.objects.filter(nom=nom_comp).first()
        if comp:
            PointsForts.objects.create(
                competences_id=comp.id,
                utilisateurs_id=user_id,
            )


def sync_points_faibles(user_id, noms_competences):
    PointsFaibles.objects.filter(utilisateurs_id=user_id).delete()
    for nom_comp in noms_competences:
        comp = Competences.objects.filter(nom=nom_comp).first()
        if comp:
            PointsFaibles.objects.create(
                competences_id=comp.id,
                utilisateurs_id=user_id,
            )

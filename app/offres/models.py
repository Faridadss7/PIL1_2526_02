# Modèles centralisés dans app.matching.models
# Import direct pour éviter la duplication
from app.matching.models import (
    Utilisateurs,
    Competences,
    OffresMentorat,
    Matching,
)

__all__ = ['Utilisateurs', 'Competences', 'OffresMentorat', 'Matching']

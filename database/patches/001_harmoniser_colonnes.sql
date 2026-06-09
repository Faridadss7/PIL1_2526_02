-- À exécuter une seule fois sur une base PostgreSQL déjà créée avec l'ancien schéma.
-- Harmonisage : Centre_interet → centre_interet (casse PostgreSQL)

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'utilisateurs' AND column_name = 'Centre_interet'
    ) THEN
        ALTER TABLE utilisateurs RENAME COLUMN "Centre_interet" TO centre_interet;
    ELSIF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'utilisateurs' AND column_name = 'centre_interet'
    ) THEN
        NULL; -- déjà harmonisé
    END IF;
END $$;

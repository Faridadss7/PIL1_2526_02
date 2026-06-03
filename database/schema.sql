DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS disponibilites;
DROP TABLE IF EXISTS competences;
DROP TABLE IF EXISTS points_forts;
DROP TABLE IF EXISTS points_faibles;
DROP TABLE IF EXISTS offres_mentorat;
DROP TABLE IF EXISTS matching;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS messages;


CREATE TABLE utilisateurs( 
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150)  UNIQUE NOT NULL,
    telephone VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(260) NOT NULL,
    photo_profil VARCHAR(260),
    filiere VARCHAR(150) NOT NULL,
    niveau VARCHAR(10) NOT NULL,
    bio TEXT,
    Centre_interet TEXT,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE disponibilites(
    id SERIAL PRIMARY KEY,
    jour VARCHAR(20),
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    heure_debut TIME,
    heure_fin TIME
);
CREATE TABLE competences(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    niveau VARCHAR(10) NOT NULL
);
CREATE TABLE points_forts(
    id SERIAL PRIMARY KEY,
    competences_id INTEGER NOT NULL REFERENCES competences(id) ON DELETE CASCADE,
    utilisateurs_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE
);
CREATE TABLE points_faibles(
    id SERIAL PRIMARY KEY,
    competences_id INTEGER NOT NULL REFERENCES competences(id) ON DELETE CASCADE,
    utilisateurs_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE
);
CREATE TABLE offres_mentorat(
    id SERIAL PRIMARY KEY,
    utilisateurs_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN('offre','demande')),
    competences_id INTEGER NOT NULL REFERENCES competences(id) ON DELETE CASCADE,
    format VARCHAR(20) NOT NULL CHECK (format IN('presentiel','en_ligne','les_deux')),
    description TEXT,
    statut VARCHAR(20) DEFAULT 'active' CHECK(statut IN('active','inactive')),
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE matching(
    id SERIAL PRIMARY KEY,
    mentor_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    mentore_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    score DECIMAL(5,2),
    statut VARCHAR(20) DEFAULT 'en_attente' CHECK(statut IN('en_attente','accepte','refuse')),
    date_matching TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE conversations(
    id SERIAL PRIMARY KEY,
    matching_id INTEGER REFERENCES matching(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    conversations_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    expediteur_id INTEGER NOT NULL REFERENCES utilisateurs(id),
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lu BOOLEAN DEFAULT FALSE
);
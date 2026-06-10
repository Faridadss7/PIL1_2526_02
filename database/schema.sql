DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS matching;
DROP TABLE IF EXISTS offres_mentorat;
DROP TABLE IF EXISTS points_faibles;
DROP TABLE IF EXISTS points_forts;
DROP TABLE IF EXISTS disponibilites;
DROP TABLE IF EXISTS competences;
DROP TABLE IF EXISTS utilisateurs;

CREATE TABLE utilisateurs( 
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(260) NOT NULL,
    photo_profil VARCHAR(260),
    filiere VARCHAR(150) NOT NULL,
    niveau VARCHAR(10) NOT NULL,
    bio TEXT,
    centre_interet TEXT,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disponibilites(
    id SERIAL PRIMARY KEY,
    jour VARCHAR(20) NOT NULL,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL
);

CREATE TABLE competences(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) UNIQUE NOT NULL,
    niveau VARCHAR(10) NOT NULL CHECK (niveau IN ('L1','L2','L3','M1'))
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


-- Niveau L1 (Semestres 1 & 2)
INSERT INTO competences (nom, niveau) VALUES
('Logique arithmetique et ses applications', 'L1'),
('Mathematiques fondamentales', 'L1'),
('Probabilite et statistique', 'L1'),
('Architecture et topologie des reseaux informatiques', 'L1'),
('Systeme d''exploitation et outils de base en informatique', 'L1'),
('Base de la programmation', 'L1'),
('Deontologie et droit lies aux TIC', 'L1'),
('Techniques d''expression ecrite et orale', 'L1'),
('Administration des reseaux sous Windows/Linux', 'L1'),
('Convergence et calcul differentiel', 'L1'),
('Projet integrateur', 'L1'),
('Mathematiques appliquees', 'L1'),
('Technologies web et infographie', 'L1'),
('Base de donnees relationnelles', 'L1'),
('Programmation Python', 'L1'),
('Anglais technique', 'L1');

-- Niveau L2 (Semestres 3 & 4)
INSERT INTO competences (nom, niveau) VALUES
('Structures algebriques et leurs applications en informatique', 'L2'),
('Approche orientee objet', 'L2'),
('Structures de donnees et applications avec C/Python', 'L2'),
('Statistiques et probabilites pour le scientifique de la donnee', 'L2'),
('Concepts et applications de l''intelligence artificielle', 'L2'),
('Aspects avances des technologies web', 'L2'),
('Bases du genie logiciel', 'L2'),
('Maintenance des appareils electroniques', 'L2'),
('Administration systemes et reseaux', 'L2'),
('Securite des systemes informatiques', 'L2'),
('Management de la securite du systeme d''information', 'L2'),
('Securite des reseaux', 'L2'),
('Programmation avancee en Java', 'L2'),
('Programmation graphique en Qt/C++', 'L2'),
('Programmation avancee en Python et R', 'L2'),
('Big data', 'L2'),
('Outils cloud de collecte et de traitement des donnees', 'L2'),
('Concepts et applications de l''apprentissage automatique', 'L2'),
('Techniques de resolution de probleme par la recherche', 'L2'),
('Gestion des projets', 'L2'),
('Communication manageriale', 'L2'),
('Anglais pour la communication scientifique', 'L2'),
('Politique de securite des systemes d''information', 'L2'),
('Commutation et routage', 'L2'),
('Audit normes de securite et gestion des risques et incidents', 'L2'),
('Securisation des reseaux sans fil', 'L2'),
('Cryptographie et applications', 'L2'),
('Programmation et manipulation des donnees', 'L2'),
('Systeme d''information decisionnelle et securite', 'L2'),
('Genie logiciel', 'L2'),
('Cycle de vie d''un logiciel et assurance qualite', 'L2');

-- Niveau L3 (Semestres 5 & 6)
INSERT INTO competences (nom, niveau) VALUES
('Formation sur une certification en science de la donnee', 'L3'),
('Developpement d''applications basees sur l''apprentissage automatique', 'L3'),
('Veille technologique', 'L3'),
('Hackathon en science de donnees/Big Data', 'L3'),
('Corporation Data analytics', 'L3'),
('Outils de resolution de problemes d''optimisation', 'L3'),
('Communication', 'L3'),
('Techniques entrepreneuriales', 'L3'),
('Stage', 'L3'),
('Redaction et soutenance de memoire', 'L3');

-- Niveau Master
INSERT INTO competences (nom, niveau) VALUES
('Python Avance', 'M1'),
('Java Avance', 'M1'),
('C++ Avance', 'M1'),
('JavaScript Avance', 'M1'),
('PHP Avance', 'M1'),
('R Avance', 'M1'),
('Scala Avance', 'M1'),
('Go Avance', 'M1'),
('Rust Avance', 'M1'),
('Swift Avance', 'M1'),
('Kotlin Avance', 'M1'),
('Math Avance', 'M1');

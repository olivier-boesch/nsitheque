-- DB Init for the first time

CREATE DATABASE IF NOT EXISTS NsiTheque;
CREATE USER IF NOT EXISTS 'nsitheque' IDENTIFIED BY 'pnXc-36pel3S3ZxkzkT3Lw';
GRANT ALL PRIVILEGES ON NsiTheque.* TO 'nsitheque'@'%';
FLUSH PRIVILEGES;

-- themes
CREATE TABLE IF NOT EXISTS Theme(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- nom du theme
    nom TEXT NOT NULL ,
    -- theme parent
    parent INTEGER
);

CREATE TABLE ZoneGeo(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- nom long
    nom TEXT NOT NULL,
    -- raccourci sur sujet
    nom_court TEXT NOT NULL
);

-- Sujets Ecrit --------------------------------------
-- sujet
CREATE TABLE IF NOT EXISTS Sujet_ecrit(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- reference sujet
    reference TEXT NOT NULL,
    -- année (4 chiffres)
    annee INTEGER NOT NULL ,
    -- jour (1,2,3 ...)
    jour INTEGER ,
    -- session (1 -> juin, 2- sept)
    session INTEGER,
    -- nom de fichier stocké (____.pdf)
    fichier TEXT NOT NULL
);

-- exercice
CREATE TABLE IF NOT EXISTS Exercice_ecrit(
    id INTEGER PRIMARY KEY  AUTO_INCREMENT,
    -- numéro dans le sujet
    numero INTEGER NOT NULL,
    -- sujet (fk)
    sujet INTEGER,
    -- étendue de l'exercice dans le sujet ( x-y )
    pages TEXT NOT NULL,
    -- étendue de l'annexe dans le sujet ( x-y ) ou NULL sinon
    annexes TEXT,
    -- nom de fichier stocké (____.pdf) ou NULL si non encore extrait
    fichier TEXT,
    FOREIGN KEY (sujet) REFERENCES Sujet_ecrit (id)
);

-- theme <-> exercice
CREATE TABLE IF NOT EXISTS Theme_Exercice_ecrit(
    -- exercice (fk)
    exercice INTEGER NOT NULL,
    -- theme (fk)
    theme INTEGER NOT NULL,
    PRIMARY KEY (exercice, theme),
    FOREIGN KEY (theme) REFERENCES Theme(id),
    FOREIGN KEY (exercice) REFERENCES Exercice_ecrit(id)
);

CREATE TABLE ZoneGeo_Sujet_ecrit(
    zonegeo INTEGER,
    sujet INTEGER,
    PRIMARY KEY (zonegeo, sujet),
    FOREIGN KEY (zonegeo) REFERENCES ZoneGeo(id),
    FOREIGN KEY (sujet) REFERENCES Sujet_ecrit(id)
);

-- Sujets Oral --------------------------------------
-- sujet
CREATE TABLE IF NOT EXISTS Sujet_oral(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- référence sujet (2 chiffres)
    Reference TEXT NOT NULL,
    -- année (4 chiffres)
    Annee INTEGER,
    -- nom de fichier stocké (____.pdf)
    fichier TEXT NOT NULL
);

-- exercice
CREATE TABLE IF NOT EXISTS Exercice_oral(
    id INTEGER PRIMARY KEY  AUTO_INCREMENT,
    -- numéro dans le sujet
    numero INTEGER NOT NULL,
    -- sujet (fk)
    sujet INTEGER,
    -- étendue de l'exercice dans le sujet ( x-y )
    pages TEXT NOT NULL,
    -- nom de fichier stocké (____.pdf) ou NULL si non encore extrait
    fichier TEXT,
    -- fichier python à compléter (pour les ex type 2) ou NULL si ex type 1
    fichier_python TEXT,
    FOREIGN KEY (sujet) REFERENCES Sujet_oral (id)
);

-- theme <-> exercice
CREATE TABLE IF NOT EXISTS Theme_Exercice_oral(
    -- exercice (fk)
    exercice INTEGER NOT NULL,
    -- theme (fk)
    theme INTEGER NOT NULL,
    PRIMARY KEY (exercice, theme),
    FOREIGN KEY (theme) REFERENCES Theme(id),
    FOREIGN KEY (exercice) REFERENCES Exercice_oral(id)
);


INSERT INTO ZoneGeo (nom, nom_court) VALUES
                                         ("Amérique du Nord", "AN"),
                                         ("Amérique du Sud", "AS"),
                                         ("Métropole", "ME"),
                                         ("Asie", "JA"),
                                         ("Centres étrangers", "G1"),
                                         ("Nouvelle Calédonie", "NC"),
                                         ("Liban", "LI"),
                                         ("Polynésie", "PO");
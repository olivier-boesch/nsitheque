-- DB Init for the first time

CREATE DATABASE IF NOT EXISTS NsiTheque;
CREATE USER IF NOT EXISTS 'nsitheque' IDENTIFIED BY 'pnXc-36pel3S3ZxkzkT3Lw';
GRANT ALL PRIVILEGES ON NsiTheque.* TO 'nsitheque'@'%';
FLUSH PRIVILEGES;

-- themes
CREATE TABLE IF NOT EXISTS Theme(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  nom TEXT NOT NULL ,
  parent INTEGER
);

-- Sujets Ecrit --------------------------------------
-- sujet
CREATE TABLE IF NOT EXISTS Sujet_ecrit(
    id INTEGER PRIMARY KEY,
    Reference TEXT NOT NULL,
    Annee INTEGER,
    fichier TEXT
);

-- exercice
CREATE TABLE IF NOT EXISTS Exercice_ecrit(
  id INTEGER PRIMARY KEY  AUTO_INCREMENT,
  numero INTEGER NOT NULL,
  sujet INTEGER,
  pages TEXT NOT NULL,
  annexes TEXT,
  fichier TEXT,
  FOREIGN KEY (sujet) REFERENCES Sujet_ecrit (id)
);

-- theme <-> exercice
CREATE TABLE IF NOT EXISTS Theme_Exercice_ecrit(
    exercice INTEGER NOT NULL,
    theme INTEGER NOT NULL,
    PRIMARY KEY (exercice, theme),
    FOREIGN KEY (theme) REFERENCES Theme(id),
    FOREIGN KEY (exercice) REFERENCES Exercice_ecrit(id)
);

-- Sujets Oral --------------------------------------
-- sujet
CREATE TABLE IF NOT EXISTS Sujet_oral(
    id INTEGER PRIMARY KEY,
    Reference TEXT NOT NULL,
    Annee INTEGER,
    fichier TEXT
);

-- exercice
CREATE TABLE IF NOT EXISTS Exercice_oral(
  id INTEGER PRIMARY KEY  AUTO_INCREMENT,
  numero INTEGER NOT NULL,
  sujet INTEGER,
  pages TEXT NOT NULL,
  annexes TEXT,
  fichier TEXT,
  FOREIGN KEY (sujet) REFERENCES Sujet_oral (id)
);

-- theme <-> exercice
CREATE TABLE IF NOT EXISTS Theme_Exercice_oral(
    exercice INTEGER NOT NULL,
    theme INTEGER NOT NULL,
    PRIMARY KEY (exercice, theme),
    FOREIGN KEY (theme) REFERENCES Theme(id),
    FOREIGN KEY (exercice) REFERENCES Exercice_oral(id)
);

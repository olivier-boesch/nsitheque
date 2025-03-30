# nsitheque

## backend (priorité)

-[ ] page login (otp)
-[ ] page ajout sujet ecrit
  -[ ] reférence sujet
  -[ ] annéee sujet
  -[ ] zone géographique 
  -[ ] upload fichier
  -[ ] informations exercices (5 exos) avec:
    -[ ] themes (checkbox)
    -[ ] pages sujet
    -[ ] pages annexes
    -[ ] numéro d'exercice dans le sujet

-[ ] page ajout sujet oral
  -[ ] reférence sujet
  -[ ] annéee sujet (année banque)
  -[ ] upload fichier
  -[ ] informations exercices (2 exos) avec:
    -[ ] themes (checkbox)
    -[ ] pages sujet
    -[ ] numéro d'exercice dans le sujet
  
### Process d'indexation

#### Écrit

- upload du fichier pdf (file)
- année de sortie (select de 2000 à année courante)
- référence EN (text input)
- Exercices:
  - pages: amplitude. ex: 2-5 (text input)
  - annexes : amplitude. ex: 2-5 -- facultatif (text input)
  - numero: place dans le sujet  (checkbox 1,2,3,4,5)
  - themes: themes associés  (série de checkbox)

#### Oral

- upload du fichier pdf (file)
- année de sortie de la banque (select de 2000 à année courante)
- référence EN (text input)
- Exercices:
  - pages: amplitude. ex: 2-5 (text input)
  - numero: place dans le sujet  (checkbox 1,2)
  - fichier python: fichier à compléter (file) (facultatif)
  - themes: themes associés  (série de checkbox)

## Frontend

-[ ] page d'accueil
-[ ] page géo
-[ ] page année
-[ ] page theme
-[ ] page recherche


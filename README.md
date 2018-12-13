# pacepo
Parce qu'Alcuin C'Est Pas Ouf

Ce programme a pour but de synchroniser l'agenda Alcuin des étudiants de l'ESAIP sur leur agenda google.

# Setup

Tout ici est décrit sous Linux/Mac. 

Pour windows:

Installez python3.x, cochez "add to PATH" + installez pip via le script https://bootstrap.pypa.io/get-pip.py (qu'il faut exécuter en double cliquant dessus par exemple, après avoir installer python bien sûr:))


Vérifier dans le PATH de Windows (Système->Paramètres système avancés->Variables d'environnement..) que les dossier 
``
C:\Users\machin\AppData\Local\Programs\Python\Python3x\Scripts\
``
 et 
 ``
C:\Users\machin\AppData\Local\Programs\Python\Python3x\
``
 sont bien dans les variables d'environnement, sinon les ajouter (bien mettre le \ à la fin).

Fin de la config windows :)

Téléchargez le repository :
```
git clone https://github.com/lyghtnox/pacepo
```
Ou cliquez sur le gros bouton vert "Clone or download"

Modifiez ensuite le fichier main.py pour qu'il correspondent à vos besoin (juste les 3 premières lignes)
```
LOGIN="" <-- Votre identifiant alcuin 
PASS=""  <-- Votre mot de passe alcuin
CALENDAR_ID=""  <-- Votre id de calendrier google
```
Pour le calendrier:

Allez sur: https://calendar.google.com/

Cliquez sur les 3 points verticaux du calendrier dans lequel vous voulez synchroniser votre agenda (dans la liste des calendriers à gauche) puis sur "Paramètres". Je vous conseille de créer un nouvel agenda ESAIP et de l'utiliser que pour ça, le programme vide le calendrier avant de synchroniser.

Copiez ensuite l'ID de l'agenda dans le programme python.

Cliquez ensuite ici: https://developers.google.com/calendar/quickstart/python

Cliquez sur "Enable the Google Calendar API"

Créez un nouveau projet (laissez le nom par défault) ou utilisez en un existant.

Téléchargez le fichier credentials.json (cliquez sur "DOWNLOAD CLIENT CONFIGURATION")

Déplacez ensuite credentials.json dans le même dossier que main.py

Installez tout et lancez:

Pour Linux/Mac:
```
python3 -m pip install -r requirements.txt
python3 main.py 7
```

Pour Windows:
```
pip -r requirements.txt
py main.py 7
```
Si tout se passe bien un lien devrait s'afficher dans le terminal, copiez le dans votre navigateur, puis copiez le code qui s'affiche dans le terminal.

Normalement ça devrait marcher

# Utilisation:

Passez en argument le nombre de jours à synchroniser. Par exemple 14:

Linux/Mac:
```
python3 main.py 14
```
Windows:
```
py main.py 14
```
# Automatisation
Pour Linux/Mac, vous pouvez créer une règle cron comme celle la:
```
0 5 * * * /home/pi/alcuin/main.py 7
```
Pour Windows:

- Ouvrez le Planificateur de tâche

- Dans le menu Action sélectionnez "Créer une tâche de base..."

- Renseignez un nom/description, Suivant >

- Choisissez le Déclencheur (Tous les jours/Semaines/Mois etc)

- Arrivé à l'étape "Action" sélectionnez "Démarrer un programme"

- Dans Programme/script sélectionnez l'exécutable Python3 qui doit se trouver par là 
```
C:\Users\machin\AppData\Local\Programs\Python\Python36\python.exe
```
 (ça doit aussi fonctionner en mettant seulement "py" logiquement vu que le lien est dans le PATH)
 
- Dans "Add Arguments" mettez le lien du script main.py suivi de l'argument, genre pour moi :
```
"C:\Users\Pingui\Desktop\pacepo-master\main.py 14"
```
Personnellement je le fait tourner sur un raspberry pi qui le lance tous les matins.

# Remerciments
Merci à [@P3t3rPan](https://github.com/P3t3rPan>) pour toute la partie sur Windows.

# Autre
Le code est pas ouf je sais j'avais pas le temps je l'améliorerais peut-être plus tard.

Si jamais quelqu'un trouve une api sur le site d'alcuin faites moi signe, le parsing d'html c'est degueu.

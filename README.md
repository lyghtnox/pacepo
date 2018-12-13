# pacepo
Parce qu'Alcuin C'Est Pas Ouf

Ce programme a pour but de synchroniser l'agenda Alcuin des étudiants de l'ESAIP sur leur agenda google.

# Setup

Tout ici est décrit sous Linux/Mac. Pour windows c'est chiant démerdez vous.

Téléchargez d'abord le repository :
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
```
python3 -m pip install -r requirements.txt
python3 main.py 7
```
Si tout se passe bien un lien devrait s'afficher dans le terminal, copiez le dans votre navigateur, puis copiez le code qui s'affiche dans le terminal.

Normalement ça devrait marcher

# Utilisation:

Passez en argument le nombre de jours à synchroniser. Par exemple 14:
```
python3 main.py 14
```
Pour automatiser, vous pouvez créer une règle cron comme celle la:
```
0 5 * * * /home/pi/alcuin/main.py 7
```
Personnellement je le fait tourner sur un raspberry pi qui le lance tous les matins.

# Autre
Le code est pas ouf je sais j'avais pas le temps je l'améliorerais peut-être plus tard.

Si jamais quelqu'un trouve une api sur le site d'alcuin faites moi signe, le parsing d'html c'est degueu.

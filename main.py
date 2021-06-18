#!/usr/bin/python3

# Author: Nathaniel Campan

from bs4 import BeautifulSoup
import requests
import sys
import re
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import argparse

#Générez les api google agenda avant toute chose: https://developers.google.com/calendar/quickstart/python
#Editez les champs ci-dessous:

LOGIN=""
PASS=""
CALENDAR_ID=""

def main(argv):

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="Synchronise Alcuin sur Google Agenda")
    parser.add_argument('days', type=int, help="Nombre de jours a synchroniser")
    parser.add_argument('-o', '--output', help="Fichier de log")

    args = parser.parse_args()

    if args.output:
        sys.stdout = open(args.output, 'w+')


    print("[*] Connexion à Alcuin")
    data, session = getInputs("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")
    session = loginAlcuin("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx", data, session)  #Connexion successful
    print("[*] Extraction des données et synchronisation sur Google Agenda")
    for delta in range(args.days):
        date = datetime.datetime.today() + datetime.timedelta(days=delta)
        print("[*] Synchronisation du {}".format(date.strftime("%d/%m/%Y")))
        cal = retrieveCal("", session, date)
        rmGoogle(delta, parser)
        for i in cal:
            calData = extractCalData(i)
            if calData:
                synchroGoogle(date, calData[0], calData[1], calData[2], calData[3], calData[4])

    print("[*] Agenda synchronisé!")

def getInputs(url): #Get the inputs to send back to the login page (Tokens etc)
    s = requests.Session()
    r = s.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    inputs = soup.find_all("input")

    data={}
    for i in inputs:    #Extract inputs and store them in data
        try:
            data[i["name"]]=i["value"]
        except:
            pass
    return(data, s)

def loginAlcuin(url,data,s):    #login
    data["UcAuthentification1$UcLogin1$txtLogin"] = LOGIN
    data["UcAuthentification1$UcLogin1$txtPassword"] = PASS
    try:
        s.post(url, data=data)
        print("[*] Connexion à Alcuin réussie")
    except:
        print("[-] Impossible de se connecter à Alcuin")
        sys.exit()
    return(s)

def retrieveCal(url, s, d):
    r = s.get('https://esaip.alcuin.com/OpDotNet/Context/context.jsx')  #Get user ID to show the right calendar
    usrId = re.search('\w+[0-9]', r.text).group(0)  #Regex to extract user ID
    data = {'IdApplication': '190', 'TypeAcces': 'Utilisateur', 'url': '/EPlug/Agenda/Agenda.asp', 'session_IdCommunaute': '561', 'session_IdUser': usrId, 'session_IdGroupe': '786', 'session_IdLangue': '1'}
    s.post("https://esaip.alcuin.com/commun/aspxtoasp.asp", data=data)  #Retrieve the calendar and create the necessary token
    r = s.post("https://esaip.alcuin.com/EPlug/Agenda/Agenda.asp", data={"NumDat": d.strftime('%Y%m%d'), "DebHor": "08", "FinHor": "18", "ValGra": "60", "TypVis":"Vis-Jrs.xsl"}) #Extract a specific day
    soup = BeautifulSoup(r.text, "html.parser")
    cal = soup.find_all("td", {"class": "GEDcellsouscategorie", "valign": None})
    return(cal)

def extractCalData(cal):
    course = cal.get_text() #Retrieve a specific course
    if os.name == 'nt':
        course = course.encode('cp1252').decode('latin9')    #Decode if os is windows
    time = []
    try:
        [time.append(re.split('H', i)) for i in re.findall('\d\dH\d\d', course)]   #[['08', '15'], ['09', '45']]
        courseSplit = re.split('- ', re.split('\d\dH\d\d', course)[0])
        courseName = courseSplit[1]

        if re.search('Examen', courseSplit[0]):
            colorId = '11'
            description = courseSplit[0]
        elif re.search('Cours', courseSplit[0]):
            colorId = '5'
            description = courseSplit[0]
        else:
            courseName = '{} - {}'.format(courseSplit[0], courseName)
            colorId = '4'
            description = courseSplit[0]

        salle1 = re.sub('[A-Z]{2,}\d','',  re.split('\d\dH\d\d', course)[-1])    #Get second part
                
        if re.search('Amphi A', course):
            salle = 'Amphi A'
        elif re.search('Amphi E', course):
            salle = 'Amphi E'
        elif re.search('[ABCEF]\d+', salle1):
            salle = re.search('[ABCEF]\d+', salle1).group(0)  #Retrieve classroom
        else:   #No classroom
            salle = 'Non renseigné'
                    
        return(time, salle, courseName, colorId, description)
    except:
        pass

def synchroGoogle(d, time, salle, courseName, colorId, description):
    store = file.Storage('token.json')  #API things
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', 'https://www.googleapis.com/auth/calendar')
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    event = {
        'summary': courseName,
        'location': salle,
        'colorId': colorId,
        'reminders.useDefault': 'True',
        'description': description,
        'start': {'dateTime': d.replace(hour=int(time[0][0]), minute=int(time[0][1])).isoformat(), 'timeZone': 'Europe/Paris'},
        'end': {'dateTime': d.replace(hour=int(time[1][0]), minute=int(time[1][1])).isoformat(), 'timeZone': 'Europe/Paris'}
        }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()    #Create event

def rmGoogle(delta, parser):
    store = file.Storage('token.json')
    creds = store.get()

    parser = argparse.ArgumentParser(
                description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                parents=[tools.argparser])
    flags = parser.parse_args(['--noauth_local_webserver'])
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', 'https://www.googleapis.com/auth/calendar')
        creds = tools.run_flow(flow, store, flags)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    now = datetime.datetime.utcnow().replace(hour=1, minute=0) + datetime.timedelta(days=delta)  # 'Z' indicates UTC time
    tomorrow = datetime.datetime.utcnow().replace(hour=1, minute=0) + datetime.timedelta(days=delta+1)
    events_result = service.events().list(calendarId=CALENDAR_ID,    #List every events of the day
                                          timeMin=now.isoformat() + 'Z',
                                          timeMax=tomorrow.isoformat() + 'Z',
                                          singleEvents=True).execute()
    events = events_result.get('items', [])

    for event in events:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()   #Delete events

def usage():
    print("Usage: main.py [-h] [-o output] days")
    
if __name__ == "__main__":
    main(sys.argv[1:])

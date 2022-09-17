#!/usr/bin/python3

#Author: Nathaniel Campan
import pdf
from bs4 import BeautifulSoup
import requests
import sys
import re
import datetime
import pytz
from icalendar import Calendar, Event
from httplib2 import Http
import os
import time
import argparse
from selenium import webdriver
import secret
import verbose
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Firefox()

LOGIN="mchouteau.ira2024"
PASS="586351c3"
global cal
cal = Calendar()
def main(argv):
    print("[*] Connexion à Alcuin")
    login_alcuin()  #Connexion successful
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Synchronise Alcuin sur Google Agenda")
    parser.add_argument('days', type=int, help="Nombre de jours a synchroniser")
    parser.add_argument('promo', type=int, help="promotion à syncroniser 0 = IRA3, 1 = IRA4")
    parser.add_argument('-o', '--output', help="Fichier de log")
    parser.add_argument('date', type=int, nargs='?', const=0, default=0, help="Nombre de jours depuis lequels on synchronise")
    
    args = parser.parse_args()
    promo = int(args.promo)
    os.system('rm -r /home/mchouteau/Feuille-temps/'+secret.ANNEE[promo])
    os.system('mkdir /home/mchouteau/Feuille-temps/'+secret.ANNEE[promo])
    if args.output:
        sys.stdout = open(args.output, 'w+')
    driver.get('https://esaip.alcuin.com/OpDotNet/Context/context.jsx')  #Get user ID to show the right calendar
    usrId = re.search('\w+[0-9]', driver.page_source).group(0)  #Regex to extract user 
    driver.get('https://esaip.alcuin.com/OpDotnet/commun/Login/aspxtoasp.aspx?url=/Eplug/Agenda/Agenda.asp?IdApplication=190&TypeAcces=Utilisateur&IdLien=5834&groupe=2483')
    print("[*] Extraction des données et création du calendrier")
    for delta in range(args.days):
        datefrom = datetime.datetime.today() + datetime.timedelta(args.date)
        date = datefrom + datetime.timedelta(days=delta)
        print("[*] Synchronisation du {}".format(date.strftime("%d/%m/%Y")))
        cal = retrieveCal(date,promo)
        for i in cal:
            calData = extractCalData(i)
            if calData:
                pdf.main(date.strftime('%d/%m/%Y'),  calData[0], calData[2], calData[5], date, promo)
#                print (calendrier)
#                cal.add_component(calendrier)
#                debut = datetime.datetime.strftime(debut, '%Y%m%d%H%M%S')
#                print (debut)
                build_event(date, calData[0], calData[1], calData[2], calData[3], calData[4],promo)
    print("[*] Agenda synchronisé!")

def login_alcuin():  # login
    # head to alcuin's login page
    driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")
    # find username/email field and send the username itself to the input field
    driver.find_element(By.ID, "UcAuthentification1_UcLogin1_txtLogin").send_keys(secret.LOGIN)
    # find password input field and insert password as well
    driver.find_element(By.ID, "UcAuthentification1_UcLogin1_txtPassword").send_keys(secret.PASS)
    # click login button
    driver.find_element(By.ID, "UcAuthentification1_UcLogin1_btnEntrer").click()
    try:
        assert "https://esaip.alcuin.com/OpDotNet/Noyau/Default.aspx?" == driver.current_url
        print(verbose.CONNEXIONALCUINOK)
    except:
        print(verbose.CONNEXIONALCUINNOK)
        sys.exit()

def retrieveCal(d,promo):
    driver.get("https://esaip.alcuin.com/EPlug/Agenda/Agenda.asp?NumDat="+d.strftime('%Y%m%d')+"&DebHor=08&FinHor=18&ValGra=60&NomCal="+secret.CALENDRIER[promo]+"&TypVis=Vis-Jrs.xsl")
    r = driver.page_source
    soup = BeautifulSoup(r, "html.parser")
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
        courseSplit.append(re.split('[A-Z]\d|Amphi', re.split('\d\dH\d\d', course)[2])[0])
        courseName = courseSplit[1]
        courseSplit2 = re.split('([A-Z][a-zà-ÿ]{2,}(?=[A-Z]{2,}))', courseSplit[2])
        length = len(courseSplit2)-1
        if length == 0:
            courseSplit3 = courseSplit[2]
            courseSplit[2] = courseSplit[0] + "\x0a" + courseSplit[2]
        else:
            i = 0
            courseSplit3 = ""
            while i < length:
                courseSplit3 = courseSplit3 + courseSplit2[i]
                i += 1
                courseSplit3 = courseSplit3 + courseSplit2[i] + "\x0a"
                i += 1
            courseSplit3 = courseSplit3 + courseSplit2[length]
            courseSplit[2] = courseSplit[0] + "\x0a" + courseSplit3
        if re.search('Examen', courseSplit[0]):
            colorId = '11'
            description = courseSplit[2]
        elif re.search('Cours', courseSplit[0]):
            colorId = '5'
            description = courseSplit[2]
        else:
#           courseName = '{} - {}'.format(courseSplit[0], courseName)
            courseName = courseSplit[0]
            colorId = '4'
            description = courseSplit[2]

        salle1 = re.sub('[A-Z]{2,}\d','',  re.split('\d\dH\d\d', course)[-1])    #Get second part
                
        if re.search('Amphi A', course):
            salle = 'Amphi A'
        elif re.search('Amphi E', course):
            salle = 'Amphi E'
        elif re.search('[ABCEF]\d+', salle1):
            salle = re.search('[ABCEF]\d{2,3}', salle1).group(0)  #Retrieve classroom
        else:   #No classroom
            salle = 'Non renseigné'
        return(time, salle, courseName, colorId, description, courseSplit3)
    except:
        pass

def build_event(d, time, salle, courseName,colorid, description, promo):
    filename = '/home/mchouteau/Feuille-temps/'+secret.ANNEE[promo]+'/calendrier.ics'
    event = Event()
    event.add('summary', courseName)
    event.add('description', description)
    debut = d.replace(hour=int(time[0][0]),minute=int(time[0][1]), second=0)
    fin = d.replace(hour=int(time[1][0]), minute=int(time[1][1]), second=0)
    event.add('dtstart', debut)
    event.add('dtend', fin)
    event.add('location', salle)
    cal.add_component(event)
    f = open(filename, 'wb')
    f.write(cal.to_ical())
    f.close()

def usage():
    print("Usage: main.py [-h] [-o output] days")
    
if __name__ == "__main__":
    main(sys.argv[1:])
    driver.close()

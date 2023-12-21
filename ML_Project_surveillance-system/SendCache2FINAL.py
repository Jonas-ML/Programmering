import cv2
from time import sleep
import paho.mqtt.client as mqtt
import os
import sys


#Få navne på videoer, der er gemt på devicet i specificeret mappe (path variablen)
def get_name(path):
    resultat.clear()
    for n in os.listdir(path):
        if os.path.isfile(os.path.join(path, n)):
            resultat.append(n)

#Det der sker, når maskinen får connection.
def subscribe(klient, userdata, flags, rc):
    global pathF
    #Subscriber først til states og tjek, så den kan se beskeder, der bliver sendt til de topics
    klient.subscribe(topic)
    klient.subscribe(topicTjek)
    print("forbundet")

#Laver pathF, den færdige path til videoer + navnet på første video i listen fra get_name() funktionen. Skal pakkes ind i try, da der ellers kommer IndexError
def lavPath():
    global pathF
    try:
        pathF = path + str(resultat[0])
    except IndexError:
        pass

def sendNavn():
    #Her sender den navnet på næste video i listen. Den excepter, hvis der er indexerror, og det kommer når mappen med videoer er tom. Attribute error er lidt anerledes. Meget i tvivl om, hvorfor
    #Den kom, den burde ikke komme mere, men har beholdt den for en sikkerhedsskyld.
    #Skal bruge navne på videoer (resultat liste), så lavPath kan køres derefter.
    get_name(path)
    lavPath()
    try:
        klient.publish("video", resultat[0])
    except IndexError or AttributeError:
        print("ingen videoer i mappen")
        sleep(1)
        pass

#Send video loopet
def sendVideo():
    global capTjek, Run
#Skal være i try, da der kan komme cv2 error eller attribute error. Dog er det samme problem igen med attribute error, meget i tvivl om, hvad der har triggered erroren, men er beholdt for en sikkerhedsskyld
    try:
        while Run:
            #Ret = bool. Hvis ret er false, så er der ikke flere frames tilbage. Frame er det man sender for at opbygge videoen igen.
            ret, frame = cap.read()
            #Encode af frame inden det sendes
            img_str = cv2.imencode('.jpg', frame)[1].tobytes()
            #Publisher frame til video topic
            klient.publish("video", img_str)
            #Lille sleep timer, da video begyndte at afspille ekstremt hurtigt uden.
            sleep(0.05)
    except cv2.error or AttributeError:
        print("Ikke mere data")
        #Skal sættes til false, da det er den state de starter i, når man kører scriptet. Hvis ikke, så vil scriptet ikke virke korrekt, og dermed ikke sende videoer
        capTjek = False
        Run = False

def on_message(client, userdata, msg):
    global Run, cap, capTjek
    #Alle modtagne beskeder laves om til en string, og smides ind i k
    k = str(msg.payload)
    #Hvis der kommer besked fra topicet "tjek"
    if topicTjek in msg.topic:
        #hvis der står online i beskeden, så ved den, at PC er online
        if online in k:
        #Sender navn på næste video, der skal sendes, hvis pc er online.
            sendNavn()
            sleep(1)
    # eller Hvis man får besked fra "states" topic
    elif topic in msg.topic:
        #Hvis der står send i msg, så sætter den Run = False, så man kommer ud af while loopet længere nede
        if string in k:
            #Sørger for cap kun bliver kørt en gang pr. video, da videoer ellers vil blive korrupte.
            if capTjek == False:
                cap = cv2.VideoCapture(pathF)
                #Sætter capTjek til true, så programmet ved, at den skal igang med at sende video
                capTjek = True

        #Hvis der er en delete besked i states topic, så havde modparten allerede videoen, og videoen slettes herfra.
        elif slet in k:
            if os.path.exists(pathF):
                os.remove(pathF)
    #Sender video, hvis man har modtaget en send besked fra online PC
    if capTjek == True:
        sendVideo()
    #Når funktionen sendVideo er færdig med at køre, sættes Run til False, hvilket får programmet til at gå herind, sætte Run = true, så programmet kan starte forfra
    #Derudover, så laver den cap.release(), da video ellers vil blive korrupt, hvis dette ikke gøres inden der startes en ny cap.
    #Sender også en done besked, så PC ved, den har modtaget hele videoen.
        if Run == False:
            klient.publish(topicTjek, "done")
            Run = True
            cap.release()


#Variabler til ovenover
string = "send"
online = "online"
topic = "states"
topicTjek = "tjek"
slet = "delete"
states = []
pathF = ""
capTjek = False
Run = bool

#Path til videoer, der skal sendes videre til PC
path = "C:/Users/benja/Desktop/videoer2/"

#Ip til Raspberry PI (Mosquitto Broker)
broker_ip = "192.168.1.57"

#Liste med resultater til get_name() funktionen
resultat = []

#Klient til MQTT
klient = mqtt.Client()
#Hvis man har sat adgangskode og brugernavn på mosquitto broker, specificeres de i linjen nedenunder og alle gåseøjne fjernes
"""klient.username_pw_set(username="gruppe3", password="gruppe3")"""
#Når klienten forbinder
klient.on_connect = subscribe
#Når klient får en besked
klient.on_message = on_message
#Forbind til broker med IP og standard port 1883. Hvis det er SSL er porten 8883
klient.connect(broker_ip, port = 1883)
#Vælger fil-format MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')



while True:
    klient.loop_start()



#Denne del, er det scriptet er opbygget fra. Gemt nederst i filen, hvis nu noget i scriptet skulle gå i stykker, så kan lidt hjælp forhåbentligt hentes her.
"""
while True:
    ret, frame = cap.read()
        #Fortæller programmet det skal gemme frames i specificeret mappe og binde det hele sammen til en video.
        #Viser streamen. Fjernes hvis bruges på jetson.
        #cv2.imshow('video', frame)
        #Encode af frame inden det sendes
    img_str = cv2.imencode('.jpg', frame)[1].tobytes()
        #Publisher videoen til video topic
    klient.publish("video", img_str)
        #Hvis man trykker på q, så slutter programmet
    if cv2.waitKey(1) & 0xFF == ord('q'):
        quit"""
            
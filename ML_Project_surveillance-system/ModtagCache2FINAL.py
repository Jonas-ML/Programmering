import cv2
from time import sleep
import paho.mqtt.client as mqtt
import numpy as np
import os


#Få liste af videoer, der er blevet tilsendt til dette device
def get_name(path):
    for n in os.listdir(path):
        if os.path.isfile(os.path.join(path, n)):
            resultat.append(n)



# Subscribe når forbindelse er oprettet til broker
def subscribe(klient, userdata, flags, rc):
    print("forbundet")
    #Publisher også en besked om, at den nu er online
    klient.publish(topicTjek, "online")
    klient.subscribe(topicVideo)
    klient.subscribe(topicTjek)
    klient.subscribe(topicStates)
    


#Når den får en besked
def on_message(klient, userdata, msg):
    #Sætter globale variabeler, så de kan tilgås udefra funktionen
    global gemt, videogem, videoer
    #Bare lige for, at den kun kører get name én gang pr. gang scriptet bliver kørt, da det kan fremprovokere en bug, der gemmer videoerne dobbelt (videoer er dobbelt så lange og det hele vises 2 gange)
    if videoer == False:
        get_name(path)
        videoer = True
    #Putter msg ind i k variablen
    k = str(msg.payload)
    #Hvis .mp4 er i beskeden, altså hvis det er navnet man får på videoen. (Det er første besked man modtager fra modparten)
    if extension in k:
        #Laver navnet om til dato og tid, minus en lang string af tal tilsidst. Navn vil altid være det samme, da datoer og tidspunkt skrives med 0 foran, hvis det er under 10. Eks: 09-09 eller 08 57
        navn = k[2:22]
        #Sætter path sammen med filnavnet, så man får fuld path til video
        filnavn = path + navn
        #Her tjekkes der om filen allerede er blevet sendt til PC
        if navn in resultat:
            print("Har allerede filen, fortsætter")
            #Publisher delete besked, så modparten ved, at dette device har fået denne video, så modparten ved, at den bare kan slette den originale video
            klient.publish(topicStates, "delete")
            sleep(3)
            #Sender en online besked, da det er sådan, at afsender ved, at nu er den klar til at modtage videoer. Desuden er alt on message, så programmerne SKAL modtage en besked før de gør noget.
            #Det samme gælder dette script.
            klient.publish(topicTjek, "online")

        #Hvis navnet ikke er i resultatet, så vil det sige, at videoen ikke er havnet på dette device, derfor downloades det.
        elif navn not in resultat:
            print("Video ikke downloadet, downloader nu")
            #Sætter send ind i states
            states.append("send")
            #Hvis send er i states, så ved modparten, at denne device ikke har modtaget videoen og sender derefter.
            klient.publish("states", str(states))
            #Sætter gemt til false, så if statement nedenunder kun bliver kørt, hvis videoen IKKE er downloadet. Hvis den kører det nedenunder og filen er lavet 1 gang så corruptes videofilen
            gemt = False

#Forklaret i kommentar ovenover.
    if gemt == False:
        try:
            #Video writeren kaldes her, det er den, der videoer blive korrupte, hvis den eksempelvis bliver kaldt ved en fejl, mens den er ved at skrive en video til mappen.
            videogem = cv2.VideoWriter(filnavn, fourcc, 30.0, (640,480))
        except UnboundLocalError:
            pass
        gemt = True


    else:
        #Laver msg.payload om til et array. Hvert array er en frame i videoen. Hvert tal er mellem 0-255. Hvert tal repræsentere en farve, og en pixel. Derefter opbygger den hele molivitten igen 
        besked = np.frombuffer(msg.payload, np.uint8)
        #Læser billeddata og sætter ind i variablen frame
        frame = cv2.imdecode(besked, cv2.IMREAD_COLOR)
        #Hvis besked fra tjek topic kommer
        if topicTjek in msg.topic:
            #Hvis der er "done" i staten, så ved den, at den er færdig med at modtage videoer og lukker derefter programmet. Programmet SKAL lukkes efter modtagelse af video,
            # da videon ellers bliver korrupt
            if streng in k:
                #Tømmer states og sætter varibler til deres originale tilstand, da program er færdigt og det hele skal resettes før det virker igen.
                states.clear()
                gemt = True
                #Lille sleep timer, da man kan opleve stort packet loss, hvis videogem.release() bliver brugt lidt for tidligt
                sleep(0.5)
                videogem.release()
                videoer = False
                #Sender besked online, da 
                klient.publish(topicTjek, "online")
                sleep(3)
        #her writer den videoen, hvis den excepter med NameError så betyder det, at der ingen videoer er.
        try:
            videogem.write(frame)
        except NameError:
            pass
            
#Variabler
gemt = True
streng = "done"
videoer = False
extension = ".mp4"
topicStates = "states"
topicTjek = "tjek"
topicVideo = "video"

#Liste med states, og resultat liste fra get_name funktionen
states = []
resultat = []

#path
path = "C:/Users/benja/Desktop/videoer/"

#Vælg fourcc
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#Laver klient variablen
klient = mqtt.Client()

#Her sættes kodeord osv. til, hvis dette er valgt i projektet
#klient.username_pw_set(username="gruppe3", password="gruppe3")

#Kører subscribe funktion så snart der er forbindelse til broker
klient.on_connect = subscribe

#Kører on_message hver gang den får besked fra modparten
klient.on_message = on_message

#Forbinder til broker med IP og standard port uden SSL. Med SSL (port=8883)
klient.connect("192.168.1.57", port=1883)

#Kører loop forevigt
while True:
    klient.loop_start()

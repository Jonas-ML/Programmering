import network
import machine
from machine import Pin
from umqtt.simple import MQTTClient
import ubinascii
import time

#Callback der køres når den modtager besked
def alarmCB(topic, msg):
    global alarm
    k = msg

    if "True" in k:
        alarm = True
        print("Alarm tændt")

    elif "False" in k:
        alarm = False
        print("Alarm slukket")


#Forbinder til netværk. Er lidt bedre forklaret i andre bilag
net = network.WLAN(network.STA_IF)
def forbind():
    net.active(True)
    if not net.isconnected():
        print("forbinder")
        net.connect('FTTH_DU1219', 'Derek401')
        while not net.isconnected():
            print("Prøver stadig")
            time.sleep(3)
            pass
    if net.isconnected():
        print("Du er nu forbundet IP = " + net.ifconfig()[0])
    
def sluknet():
    net.active(False)
    
forbind()

#Broker IP og port
brokerIP = "192.168.0.193"

#Alarm sættes til en boolean, da den enten er true eller false, og så man ikke får error i main loop, når program starter
alarm = bool

#topic 
topic = "alarm"
#Klient id
client_id = ubinascii.hexlify(machine.unique_id())
#MQTT klient
client = MQTTClient(client_id, brokerIP)

#Forbinder til broker
client.connect()

#Subscribe til alarm og sæt callback, så den ved om alarmen er blevet slået til/fra gennem dashboard
client.set_callback(alarmCB)
#Subscriber til alarm topic
client.subscribe(topic)

#Her sættes password
pw = ["1","2","3","4"]
#Liste hvor de tal man selv trykker kommer ind i, så den kan sammenligne
trykpw = []

#GPIO pins til keypadden. Det er forbindelserne der kører hen af de fire rækker på keypadden
L1 = 13
L2 = 12
L3 = 22
L4 = 33

#GPIO pins til keypadden. Det er forbindelserne der kører hen af de fire kolonner på keypadden
C1 = 15
C2 = 32
C3 = 14
C4 = 21

#Sætter dem i lister
row_pins = [L1, L2, L3, L4]
col_pins = [C1, C2, C3, C4]

#Sætter alle række pins til at være et output
for row_pin in row_pins:
    Pin(row_pin, mode=Pin.OUT)

#Sætter alle kolonne pins til at være input, og til at have en software defineret pull down modstand
for col_pin in col_pins:
    Pin(col_pin, mode=Pin.IN, pull=Pin.PULL_DOWN)

#Indsæt delay til at forebygge prel en smule.
delay = 300

#Læser keypad inputs. Det er sat op i en matrix. Når der kommer en elektrisk forbindelse fra en af kolonnerne, trækkes signalet lavt på specifikke GPIO pins, og udfra det,
#kan programmet regne ud, hvilken knap, der bliver trykket på og sættes ind i listen med password
def read_line(line, characters):
    global  tryk
    Pin(line, mode=Pin.OUT, value=1)
    
    if Pin(C1).value() == 1:
        tidnu = time.ticks_ms()
        #Det er i disse inhakkede if statements, hvor delay bliver brugt
        if tidnu - tryk > delay:
            print(characters[0])
            trykpw.append(characters[0])
            tryk = tidnu


    if Pin(C2).value() == 1:
        tidnu = time.ticks_ms()
        #Deleay
        if tidnu - tryk > delay:
            print(characters[1])
            trykpw.append(characters[1])
            tryk = tidnu
            print(trykpw)
    if Pin(C3).value() == 1:
        tidnu = time.ticks_ms()
        #delay
        if tidnu - tryk > delay:
            print(characters[2])
            trykpw.append(characters[2])
            tryk = tidnu
            print(trykpw)
    if Pin(C4).value() == 1:
        tidnu = time.ticks_ms()
        #delay
        if tidnu - tryk > delay:
            print(characters[3])
            trykpw.append(characters[3])
            tryk = tidnu
            print(trykpw)
    Pin(line, mode=Pin.OUT, value=0)

#Tryk variabel skal lige sættes til 0, så program ikke crasher
tryk = 0




#Main loop
try:
    while True:
        #Tjekker beskeder
        client.check_msg()
        #Hvis password matcher og alarmen er slået fra, så tændes alarmen
        if trykpw == pw and alarm == False:
            print("Tændt")
            client.publish(topic, "True")
            alarm = True
            trykpw.clear()
        #Hvis password matcher og alarm er slået til, så slukkes alarmen
        elif trykpw == pw and alarm == True:
            print("slukket")
            client.publish(topic, "False")
            alarm = True
            trykpw.clear()
        #Hvis man skriver forkert, skal man trykke på *, så slettes de input man har skrevet, hvis man skriver forkerta
        if "*" in trykpw:
            trykpw.clear()
        
        #Læser alle rækker hele tiden, og venter på signalet bliver trukket lavt et sted.
        read_line(L1, ["1", "2", "3", "A"])
        read_line(L2, ["4", "5", "6", "B"])
        read_line(L3, ["7", "8", "9", "C"])
        read_line(L4, ["*", "0", "#", "D"])
        time.sleep(0.1)

#For at stoppe programmet med ctrl + c, da det noglegange var svært i programmet "Thonny" med deres indbyggede
except KeyboardInterrupt:
    print("\nApplication stopped!")
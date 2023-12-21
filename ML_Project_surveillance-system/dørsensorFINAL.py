import network
from time import sleep
import machine
from machine import Pin
import time
from umqtt.simple import MQTTClient
import ubinascii


#Skal tænde alle kameraer i huset, og begynde at filme
def startFilm():
    print("Filmer")

#Hvis vindue/dør bliver åbnet og alarmen er til, så begynder kamera at filme
def alarmCB(topic, msg):
    k = msg
    if "True" in k and dor_value == 1:
        startFilm()

#Laver en net variabel
net = network.WLAN(network.STA_IF)
#Bruger led, der er forbundet til pin 13 på selve esp
led =machine.Pin(13, machine.Pin.OUT)
#Forbind til net funktionen
def forbind():
    net.active(True)
    if not net.isconnected():
        print("forbinder")
        #Skift ud med navn på netværk og kodeord
        net.connect('SSID', 'PASSWORD')
        #Når den ikke er forbundet til nettet, så lyser LED
        while not net.isconnected():
            print("Prøver stadig")
            led.value(1)
            sleep(3)
            pass
    #Når den er forbundet slukker LED
    if net.isconnected():
        led.value(0)
    #Printer IP på ESP
    print("Du er nu forbundet IP = " + net.ifconfig()[0])
#Hvis man skulle slukke nettet, bliver dog ikke brugt    
def sluknet():
    net.active(False)
    led.value(0)

#Funktionskald 
forbind()

#Broker IP
brokerIP = "192.168.0.193"


#topic
topic = "sensor"
#Klient ID, der skal specificeres ellers kan man ikke forbinde til broker. Skal ikke gøres i paho mqtt, måske den gør selv bag alt koden?
client_id = ubinascii.hexlify(machine.unique_id())
#Klient sættes sammen med client id og broker ip
client = MQTTClient(client_id, brokerIP)
#Forbinder til broker
client.connect()

#Sætter callback til alarmCB funktionen. Den kører funktionen, så snart den modtager besked. Samme som on_message i paho
client.set_callback(alarmCB)
#Subscriber til alarm topic
client.subscribe("alarm")

#Pin 32 bliver brugt til dør/vinduessensoren
pin = 32
#dor variabel hvor pin, Pin input og pull up modstand specificeres
dor = Pin(pin, Pin.IN, Pin.PULL_UP)

#Program loop
while True:
    #dor_value variabel bliver det samme som dor_value(), altså når spænding er høj = 1, spænding er lav = 0
    dor_value = dor.value()
    #Tjekker for beskeder
    client.check_msg()
    #Når spænding er høj, så er døren åben
    if dor_value == 1:
        client.publish(topic, "open")
    #Når spænding er lav, er døren lukket
    elif dor_value == 0:
        client.publish(topic, "closed")
    
    #Sleep så den ikke spammer
    sleep(5)
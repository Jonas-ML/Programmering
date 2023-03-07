import serial
import logging
from time import sleep
import RPi.GPIO as GPIO
from dragino import Dragino
import binascii

GPIO.setwarnings(False)
D = Dragino("dragino.ini", logging_level=logging.DEBUG)
D.join()
while not D.registered():
    print("Waiting")
    sleep(2)




S = serial.Serial("/dev/ttyS0")

#Sætter globale variabler, der vil blive brugt senere
substreng = "GGA"
substreng2 = "N"
substreng3 = "S"
substreng4 = "E"
substreng5 = "W"
north = float(1)
south = float(-1)
east = float(1)
west = float(-1)



#Loop
while True:
    #Den vil prøve dette, hvis ikke, så excepter den. Det er højst sandsynligt pga. dragino ikke er opstartet helt endnu
    try:
        #Læser data fra GPS og sætter ind i variablen streng
        streng = S.readline().decode().strip("\n")
        #Den tjekker alt data fra GPS, men kun dem der er GGA data
        if substreng in streng:
            #Her tjekker den om der er nord eller syd i dataen for at finde ud af om man skal multiplicere x med -1 eller 1
            if substreng2 or substreng3 in streng:
                if substreng2 in streng:
                    x = float(streng[18:20]) + (float(streng[20:27]) / 60) * north
                    roundedX = round(x, 4)
                    
                    
                else:
                    x = float(streng[18:20]) + (float(streng[20:27]) / 60) * south
                    roundedX = round(x, 4)
                    
                    
            #Her tjekker den om der er vest eller syd i dataen, så man ved om Y skal multipliceres med 1 eller -1
            if substreng4 in streng or substreng5 in streng:
                if substreng4 in streng:
                    y = float(streng[30:33]) + (float(streng[33:40]) / 60) * east
                    roundedY = round(y,4)
                    
                    
                else:
                    y = float(streng[30:33]) + (float(streng[33:40]) / 60) * west
                    roundedY = round(y,4)
                
           
            D.send(roundedX)
            sleep(1)
            D.send(roundedY)
            sleep(1)
    except:
        print("No coordinates sent yet, dragino might not be fully connected at this time. Please wait a few minutes and try again.")            
                



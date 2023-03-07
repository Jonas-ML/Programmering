# -*- coding: utf-8 -*-
import socket
import RPi.GPIO as GPIO
import pygame
from rover import forwards, motor1, motor2, motor3, motor4,halt , left, right, cutl,cutr, backwards

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
chan_list = [16,20,26,21]
GPIO.setup(chan_list, GPIO.OUT)

motor1.start(0)
motor2.start(0)
motor3.start(0)
motor4.start(0)

print("Kører serveren\n")

host = "0.0.0.0" # Dette er IP-adressen for Raspberry Pi
port = 3000 # Husk at portnumre på 1024 og lavere er priviligerede

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Man kan give argumenter til denne (f.eks. om det skal være TCP eller UDP)
skt.bind((host, port)) # Tilskriver IP-adressen og porten til vores socket

while True:
    data, adresse = skt.recvfrom(64)
    dekodet_data = data.decode("UTF-8")

    if data:
        print("Data modtaget: ", str(dekodet_data))
        skt.sendto(data, adresse)
        if str(dekodet_data) =="forwards":
            forwards()
        elif str(dekodet_data)=="stop":
            halt()
        if str(dekodet_data)=="backwards":
            backwards()
        elif str(dekodet_data)=="stop":
            halt()
        if str(dekodet_data) =="left":
            left()
        elif str(dekodet_data)=="cutl":
            cutl()
        if str(dekodet_data) =="right":
            right()
        elif str(dekodet_data)=="cutr":
            cutr()
    else:
        print("Ikke mere data.")
        break
skt.close()


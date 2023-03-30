#!/usr/bin/env python

#import libaries and modules
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pyttsx3
engine = pyttsx3.init()
import RPi.GPIO as GPIO

#disable any gpio warnings
GPIO.setwarnings(False)

#set up the rfid reader
reader = SimpleMFRC522()

try:
        #id, text = reader.read()

        #read the id of the tag
        id = reader.read_id()
        print(id) #print the id
finally:
        GPIO.cleanup() #clean up the gpio pins
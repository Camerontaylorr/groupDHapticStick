         #!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pyttsx3
engine = pyttsx3.init()
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
reader = SimpleMFRC522()

try:
        id, text = reader.read()
        id = reader.read_id()
        print(id)
       # engine.say("You are in " + text)
        print("You are in " + text)
       # engine.runAndWait()
finally:
        GPIO.cleanup()
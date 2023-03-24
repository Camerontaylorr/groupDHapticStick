#Group D - Haptic Stick Main Code

#Imports for modules & libaries
import RPi.GPIO as GPIO
#import time as my_time
from mfrc522 import SimpleMFRC522
import pyttsx3
from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
import subprocess
import sys
import os
import time
import time as my_time
from time import sleep
import subprocess

# Initialize pyttsx3 and PWMOutputDevice
engine = pyttsx3.init()
motor = PWMOutputDevice(21)

# Set up GPIO pin numbering
GPIO.setmode(GPIO.BCM)


# Set up pin 16 as an input pin with a pull-up resistor
button_pin = 16
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button_pin1 = 17
GPIO.setup(button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button_pin2 = 12
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO_TRIGGER = 4
GPIO_ECHO = 14

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def run_command(command):
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 5):
        print('ERROR: Requires Python 3.5 or later -- try updating/running python3')

    if os.name == 'nt':
        print('ERROR: os.set_blocking() not supported on Windows')

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd='.', shell=False)
    os.set_blocking(proc.stdout.fileno(), False)
    while proc.poll() is None:
        yield proc.stdout.readline().strip()

# Set up the RFID reader
reader = SimpleMFRC522()

#variable for saying the distance just once
beacon_a = 9999
beacon_b = 9999
beacon_c = 9999
print (float(beacon_a))
last_distance = ""

# Define a dictionary that maps RFID tag IDs to room names
room_names = {
    584189697976: "Main Entrance",
    584190220710: "Discussion Area",
    584189710965: "Toilet",
    584189995784: "Teaching Room",
    584185988475: "Pantry",
    584192553704: "Pantry",
    584189712240: "Bobs Room",
    584189996047: "Pantry",
    584192554222: "Main Entrance",
    584183290140: "Pantry"
}

# Define a dictionary that maps RFID tag IDs to turn directions
directions = {
    #584183290140: "Right"
}

# Global variable to store the text of the last scanned RFID tag
last_tag_text = ""
last_room_name = "" # Initialize the last room name to an empty string
room1 = False
room2 = False
# Function to calculate the vibration level based on time
def calculate_vibration(time):
    if time <= 0:
        return 0
    elif time >= 1:
        return 1
    else:
        return ((t - 0.02) / 3.98)

last_id = None
# Function to read the RFID tag
def rfidReader():
    global last_tag_text
    global last_id
    global room1

    id = reader.read_id_no_block()
    if id == last_id:
        return
    print("SCAN: " + str(id) + " -- previously: " + str(last_id))
    last_id = id
    if not id:
        return

    if id in room_names:
        # If the RFID tag is recognized, store the corresponding room name in last_tag_text
        room_name = room_names[id]
        print(id, flush=True)
        last_tag_text = room_name
        message = "You are in " + room_name

        # Vibrate the motor for 2 seconds
        vibration = calculate_vibration(1)
        motor.value = vibration
        my_time.sleep(0.5)
        vibration = calculate_vibration(0)
        motor.value = vibration
        print(message)
        engine.say(message)
        engine.runAndWait()
        # If the room is associated with a turn direction, say the direction
    if id in directions:
        # If the room is associated with a turn direction, say the direction
        print("Turn " + directions[id])
        engine.say("Turn " + directions[id])
        engine.runAndWait()

    if (room_name == "Bobs Room"):
        room1 = True;
# Function to handle button press
def button_callback(channel):
    global last_tag_text, last_room_name

    if not GPIO.input(button_pin):
        print("Button pressed")
        if last_tag_text:
            if last_tag_text == "left":
                # If the last scanned RFID tag was "left", say the previous room's name instead
                if last_room_name:
                    lastRoom = "You are in: " + last_room_name
                    print(lastRoom)
                    engine.say(lastRoom)
                    engine.runAndWait()
            else:
                last_room_name = last_tag_text
                print("You are in: " + last_tag_text)
                engine.say("You are in: " + last_tag_text)
                engine.runAndWait()
        else:
            print("No place")
# Add event listener to detect button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# TODO: Work out what to say based on the known beacon distances
def get_distance():
    distance1 = round(float(beacon_a)*100)
    distance2 = round(float(beacon_b)*100)
    if (room1 == False):
        if distance1 < 50:
            return "Pantry is close"
        elif distance1 < 100:
            return "Pantry is at a medium distance"
        elif distance1 > 100:
            return "Pantry is far away"

    if (room1 == True and room2 == False):
        if distance2 < 50:
            return "Bobs room is close"
        elif distance2 < 100:
            return "Bobs room is at a medium distance"
        elif distance2 > 100:
            return "Bobs room is far away"

    if beacon_c < beacon_a and beacon_c < beacon_b:
        return "Beacon C is " + str(beacon_a) + " metres away"
    return "You are not near any beacons"

# Function to handle button press for getting the distance
def button_callback1(channel):
    if not GPIO.input(button_pin1):
        print("Button pressed 2")
        print("close")
        distance = get_distance()
        engine.say(distance)
        engine.runAndWait()
GPIO.add_event_detect(button_pin1, GPIO.FALLING, callback=button_callback1, bouncetime=300)

def get_obstacle():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

  # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    obstacle = (TimeElapsed * 34300) / 2
    return obstacle

# Function to handle button press for getting the distance
def button_callback2(channel):
    if not GPIO.input(button_pin2):
        print("Button pressed 6")
        obstacle = get_obstacle()
        print (obstacle)
        if(obstacle < 10):
            obstacle = ("Obstacle Ahead")
            engine.say(obstacle)
            engine.runAndWait()
        else:
            obstacle = ("Coast is Clear")
            engine.say(obstacle)
            engine.runAndWait()

GPIO.add_event_detect(button_pin2, GPIO.FALLING, callback=button_callback2, bouncetime=300)

# Run the scan and extract the distance from the output
for line in run_command(['node', 'scan.mjs']):
    if line is None or line == "":
        print('...waiting...')
        sleep(.250)
    else:
        print('READ: ' + line)
        parts = line.strip().split(',')
        beacon = parts[0]
        distance = float(parts[1])
        if beacon == "fbe2f9bfa973":
            beacon_a = distance
            print('BEACON-A: ' + beacon + ' at ' + str(round(float(beacon_a)*100)) + 'cm')
        elif beacon == "f13efda77196":
            beacon_b = distance
            print('BEACON-B: ' + beacon + ' at ' + str(distance) + 'm')
        elif beacon == "???":
            beacon_c = distance
            print('BEACON-C: ' + beacon + ' at ' + str(distance) + 'm')
        else:
            #print('BEACON-?: ' + beacon + ' at ' + str(distance) + 'm')
            pass
    print(room1)
    rfidReader()
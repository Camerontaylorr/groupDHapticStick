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
button_pin1 = 12
GPIO.setup(button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button_pin2 = 3
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO_TRIGGER = 4
GPIO_ECHO = 17

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
last_distance = ""

# Define a dictionary that maps RFID tag IDs to room names
room_names = {
    584189697976: "Room 1",
    584190220710: "Room 2",
    584189710965: "Room 3",
    584189995784: "Room 4",
    584185988475: "Room 5",
    584192553704: "Room 7",
    584189712240: "Room 8",
    584189996047: "Room 9",
}

# Define a dictionary that maps RFID tag IDs to turn directions
directions = {
    584192554222: "Left",
    584183290140: "Right"
}

# Global variable to store the text of the last scanned RFID tag
last_tag_text = ""
last_room_name = "" # Initialize the last room name to an empty string

# Function to calculate the vibration level based on time
def calculate_vibration(time):
    if time <= 0:
        return 0
    elif time >= 1:
        return 1
    else:
        return ((t - 0.02) / 3.98)

# Function to read the RFID tag
def rfidReader():
    global last_tag_text

    id, text = reader.read()

    if id in room_names:
        # If the RFID tag is recognized, store the corresponding room name in last_tag_text
        room_name = room_names[id]
        last_tag_text = room_name
        message = "You are in " + room_name

        # Vibrate the motor for 2 seconds
        vibration = calculate_vibration(1)
        motor.value = vibration
        my_time.sleep(0.5)
        vibration = calculate_vibration(0)
        motor.value = vibration
        print(message)
        flush=True
        engine.say(message)
        engine.runAndWait()
        # If the room is associated with a turn direction, say the direction
    if id in directions:
        # If the room is associated with a turn direction, say the direction
        print("Turn " + directions[id])
        engine.say("Turn " + directions[id])
        engine.runAndWait()

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

def get_distance():
    # Run the scan and extract the distance from the output
    for line in run_command(['node', 'scan.mjs']):
        if line is None or line == "":
            #print('...waiting...')
            sleep(.250)
        else:
            print('READ: ' + line)
            distance = str(line.strip())
            return distance

# Function to handle button press for getting the distance
def button_callback1(channel):
    if not GPIO.input(button_pin1):
        print("Button pressed")
        distance = get_distance()
        engine.say("Distance: " + format(distance))
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
        print("Button pressed")
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

# Keep the program running forever
while True:
    rfidReader()
    my_time.sleep(1.0)
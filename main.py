#Group D - NaviCane Main Code

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


# Set up pins for input pin with a pull-up resistor
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

# Define function to run shell command
def run_command(command):
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 5):
        print('ERROR: Requires Python 3.5 or later -- try updating/running python3')

    if os.name == 'nt':
        print('ERROR: os.set_blocking() not supported on Windows')
    # Open a new process to run the command and capture its output
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd='.', shell=False)
    # Set the output stream to non-blocking mode
    os.set_blocking(proc.stdout.fileno(), False)
    # Continuously read lines from the process output until it exits
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

#boolean values to check what room has been scanned
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
    global last_tag_text #stores the last tagged room name
    global last_id #stores the last tagged room ID
    global room1

    id = reader.read_id_no_block() #reads the ID of the RFID tag
    if id == last_id: #if the ID is the same a the last ID, do nothing
        return
    #print the ID of the scanned tag and the previous
    print("SCAN: " + str(id) + " -- previously: " + str(last_id))
    last_id = id #updates the previous ID with the current ID
    #if there is no ID return nothing
    if not id:
        return

    if id in room_names:
        # If the RFID tag is recognized, store the corresponding room name in last_tag_text
        room_name = room_names[id] #get the room name associated with the ID
        print(id, flush=True) #get the ID of the scanned tag
        last_tag_text = room_name #Store the room name in the global variable 'last_tag_text'
        message = "You are in " + room_name # Create a message to be spoken


        # Vibrate the motor for 2 seconds
        vibration = calculate_vibration(1)
        motor.value = vibration
        my_time.sleep(0.5)
        vibration = calculate_vibration(0)
        motor.value = vibration
        #gives the audio feedback
        print(message)
        engine.say(message) #say the audio message
        engine.runAndWait() #wait for the text to speech to finish talkign
        # If the room is associated with a turn direction, say the direction
    if id in directions:
        # If the room is associated with a turn direction, say the direction
        print("Turn " + directions[id])
        engine.say("Turn " + directions[id])
        engine.runAndWait()

    if (room_name == "Main Entrance"):
        room1 = True;

# Function to handle button press
def button_callback(channel):
    global last_tag_text, last_room_name

    if not GPIO.input(button_pin):
        print("Button pressed") #test to see if button works
        if last_tag_text:
            if last_tag_text == "left":
                # If the last scanned RFID tag was "left", say the previous room's name instead
                if last_room_name: #if the last room name is known
                    lastRoom = "You are in: " + last_room_name #set the last room name to this
                    print(lastRoom)
                    engine.say(lastRoom) #say the room name
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

#function to get distance
def get_distance()
    #convert the distance from the beacons to centimeters
    distance1 = round(float(beacon_a)*100) #distance from beacon A
    distance2 = round(float(beacon_b)*100) #distance from beacon B

    #determine the distance based on the room that the user is in
    if (room1 == False):
        #if statements to determine the message that users should get based on their distance
        if distance1 < 50:
            return "Main Entrance is close"
        elif distance1 < 100:
            return "Main Entrance is at a medium distance"
        elif distance1 > 100:
            return "Main Entrance is far away"

    if (room1 == True and room2 == False):
        if distance2 < 50:
            return "Lobby is close"
        elif distance2 < 100:
            return "Lobby is at a medium distance"
        elif distance2 > 100:
            return "Lobby is far away"

    if beacon_c < beacon_a and beacon_c < beacon_b:
        return "Beacon C is " + str(beacon_a) + " metres away"
    return "You are not near any beacons"

# Function to handle button press for getting the distance
def button_callback1(channel):
    if not GPIO.input(button_pin1): #if the button is pressed
        print("Button pressed 2")
        print("close")
        distance = get_distance() #get the distance from the beacon
        engine.say(distance) #say the distance
        engine.runAndWait()
#detect if the button has been pressed
GPIO.add_event_detect(button_pin1, GPIO.FALLING, callback=button_callback1, bouncetime=300)

#function for getting obstacles
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
    # and divide by 2 due to going there and back
    obstacle = (TimeElapsed * 34300) / 2
    return obstacle

# Function to handle button press for getting the obstacles
def button_callback2(channel):
    if not GPIO.input(button_pin2): #if the button is pressed
        print("Button pressed 3") #message to check the button has been pressed
        obstacle = get_obstacle() #get the obstacle value
        print (obstacle)
        #check if the obscatle value is less than 10
        if(obstacle < 10):
            #inform user obstacle is ahead
            obstacle = ("Obstacle Ahead")
            engine.say(obstacle)
            engine.runAndWait()
        else:
            #if the value is greater than 10 inform the user that they are safe
            obstacle = ("Coast is Clear")
            engine.say(obstacle)
            engine.runAndWait()

#detect if button has been pressed
GPIO.add_event_detect(button_pin2, GPIO.FALLING, callback=button_callback2, bouncetime=300)

# Run the scan and extract the distance from the output
for line in run_command(['node', 'scan.mjs']):
    #check if the line is empty
    if line is None or line == "":
        #if line is empty print that an output is being waited for
        print('...waiting...')
        sleep(.250)
    else:
        print('READ: ' + line)
        #split parts into two
        parts = line.strip().split(',')
        # Extract the beacon and distance values from the parts list
        beacon = parts[0]
        distance = float(parts[1])

        #Check which beacon was detected and assign the distance to the corresponding variable
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
    # Print the value of the "room1" variable to the console
    print(room1)

    # Call the "rfidReader()" function to allow for tags to be scanned
    rfidReader()
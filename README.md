# groupDHapticStick
The Navicane is a white cane modified with variety of sensors to help with visually impaired indoor navigation. The Navicane makes use of a Raspberry Pi 4B, 3 BBC Microbits and RFID scanner along with NFC tags.

# General Information
The Navicane is an innovative assistive technology solution designed to help visually impaired users navigate indoor environments with ease. By utilizing RSSI signals emitted by BBC microbits, the Navicane acts as a guide, directing users towards the appropriate NFC tags that provide information about their current location.

To enhance the user experience, the Navicane incorporates a variety of sensors that provide real-time updates about the user's surroundings. With its user-friendly interface, the Navicane is accessible even to those with limited technical experience.

# Hardware 
* 1x RFID-RC522 Scanner 
* 10x NTAG213 NFC stickers
* 1x Ultrasonic sensor 
* 3x Buttons
* 3x BBC Micro:bits 
* 1x Vibration Motor 

# Software Requirements
* Python for main code and RFID reading
* Javascript for scanning for eddystone beacons 

# Libaraies and Modules
For Python
* RPi. GPIO
* mfrc522
* pyttsx3 
* gpiozero
* subprocess
* sys
* os 
* time
* sleep

# Initial Setup
1. To initalise the Navicane, you will first need to get the eddystone ID from each of the Microbits from the scanforeddystoneID file, which will then be required to be inserted into the scan.MJS file. 
2. Once these IDs have been inputted you must then get the apprioate ID's from the NFC tags, from the readRFID.py file and insert them into the Array at the start of the main.py file and give them names to your choosing 

# Using the Cane
Once the inital set up has been complete you can then start using the Navicane.
1. Place the microbits and NFC tags in your desired locations
2. Press the second button to get an approximate distance of either "close", "medium" or "far away" of the microbit
3. Keep walking towards the Microbit pressing the button when you deem neccessary
4. Press the top button to check if there are any obsctacles in your way
5. Once you arrive at NFC tag you will be informed that you are in whatever name you decided for the ID
6. Once you arrive the last NFC tag you will be informed that you have arrived

import paho.mqtt.client as mqtt # Import the MQTT library

import RPi.GPIO as GPIO

import time

from time import gmtime, strftime

PIR = 36

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR, GPIO.IN)

ourClient = mqtt.Client("makerio_mqtt") # Create a MQTT client object

ourClient.connect("172.20.240.121", 1883) # Connect to the test MQTT broker

ourClient.loop_start() # Start the MQTT client

 

# Main program loop

try:
    time.sleep(1) # Sleep for a second
    while True:
        time.sleep(0.5)
        if (GPIO.input(PIR) == 1):
            msg = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#            message = str( strftime("%Y-%m-%d %H:%M:%S", gmtime() ) )
#            message = "Motion detected", "Time:",strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ourClient.publish("data", msg) # Publish message to MQTT broker
            print("msg sent to broker")
            print(msg)

except KeyboardInterrupt:
    GPIO.cleanup()

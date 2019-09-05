import RPi.GPIO as GPIO
import time

from time import gmtime, strftime

PIR1 = 40
PIR2 = 38

GPIO.setwarnings(True)
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR1, GPIO.IN)
GPIO.setup(PIR2, GPIO.IN)

count=0

active1 = False
active2 = False

directions = []

try:
#    time.sleep(5)
    
    while True:
        time.sleep(0.7)
        if (GPIO.input(PIR1) == 1 and active2 is not True):
            active1 = True

        elif (GPIO.input(PIR1) == 1 and active2):
            active2 = False
            active1 = False
            print("direct from 2 detected")
#            directions.append("direc from 2")
            
        elif(GPIO.input(PIR2) == 1 and active1 is not True):
            active2 = True
            
        elif(GPIO.input(PIR2) == 1 and active1):
            active1 = False
            active2 = False
            print("direct from 1 detected")
#            directions.append("direc from 1")
        else:
            print("No motion detected")
            print(active1, active2)
#            print("Time:",strftime("%Y-%m-%d %H:%M:%S", gmtime()),"Count:",count)
#            print(directions)
#            print("active1:", active1, "active2:",active2) 
except KeyboardInterrupt:
    GPIO.cleanup()
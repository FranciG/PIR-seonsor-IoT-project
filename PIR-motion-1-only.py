import RPi.GPIO as GPIO
import time

from time import gmtime, strftime

PIR = 40

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR, GPIO.IN)

try:
#    time.sleep(5)
    
    while True:
#        time.sleep(0.7)
        if (GPIO.input(PIR) == 1):
            print("Motion detected")

        else:
            print("No motion detected")
#            print("Time:",strftime("%Y-%m-%d %H:%M:%S", gmtime()))
except KeyboardInterrupt:
    GPIO.cleanup()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.IN) #PIR

try:
    while True:
        if GPIO.input(36):
            print("Motion Detected...")

        else:
            print("Detecting...")
except:
    GPIO.cleanup()

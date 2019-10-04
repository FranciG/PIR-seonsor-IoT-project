#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

def get_distance():
    print ("Calculating distance")
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print ("Distance:",distance,"cm")
    return distance


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11
PIR = 40

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(PIR, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)

print ("Settling down sensors...")
timeArray = []
resetCounter = 0
time.sleep(2)

try:
      while True:
          if (GPIO.input(PIR) == 1):
              print("motion detected")
#              os.system('fswebcam -r 640x480 -S 10 --jpeg 70  −−set brightness=100%  --save /home/pi/Desktop/pic/%H%M%S.jpg')
              
#          else:
#              print("")
##              measured = get_distance()
##              timeArray.append(measured)
              
except KeyboardInterrupt:
    GPIO.cleanup()

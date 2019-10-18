#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11
PIR = 40

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(PIR, GPIO.IN)

def get_distance():
    print ("Calculating distance")
#    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
#    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    GPIO.output(PIN_TRIGGER, True)
#    time.sleep(0.00001)
    time.sleep(0.01)
    GPIO.output(PIN_TRIGGER, False)

    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()
        
    try:
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
    except:
        return;

#    print ("Distance:",distance,"cm")
    return distance
def get_direction(array):
    avg = sum(array)/float( len(array) )
    for i in array:
        standard = avg/2
        if(i < standard):
            firstSpotted = array.index(i)
            totalHalf = len(array) / 2
            if(firstSpotted < totalHalf):
                print("Direction from ultra sonic pointing")
            else:
                print("Direction from opposite of ultra sonic pointing")
    
print ("Settling down sensors...")
time.sleep(2)
try:
      while True:
          if (GPIO.input(PIR) == 1):
              print("motion detected")
              distanceArray = []
              
              while GPIO.input(PIR) == 1:
                  distance = get_distance()
                  distanceArray.append(distance)
              
              get_direction(distanceArray)
              time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()


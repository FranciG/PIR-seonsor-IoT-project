import paho.mqtt.client as mqttClient # Import the MQTT library
import RPi.GPIO as GPIO
import time
from urllib.request import urlopen
import urllib.error
from time import gmtime, strftime

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
        print("Connected to broker") 
        global Connected                #Use global variable
        Connected = True                #Signal connection  
    else:
        print("Connection failed") 
Connected = False   #global variable for the state of the connection
broker_address= "172.20.240.120"
port = 1883
user = "ubuntu"
password = "oamklinux2019"

PIR = 36

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR, GPIO.IN)

def wait_for_internet_connection():
    while True:
        try:
            response = urlopen('http://172.20.240.120/',timeout=1)
            return
        except urllib.error.URLError as e:
            ResponseData = e.reason
            print(ResponseData)
            pass

wait_for_internet_connection()

client = mqttClient.Client()               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 

# Main program loop
def main():
    try:
        time.sleep(1) # Sleep for a second
        while True:
            time.sleep(0.5)
            if (GPIO.input(PIR) == 1):
                print("motion detected")
                msg = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                client.publish("data/test",msg)
    except KeyboardInterrupt:
        GPIO.cleanup()
main()


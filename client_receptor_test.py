import paho.mqtt.client as mqttClient # Import the MQTT library

broker_address= "172.20.240.120"
port = 1883

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code " (rc))

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_adress, port)

#https://mntolia.com/mqtt-python-with-paho-mqtt-client/#1_Establishing_Connection_To_A_MQTT_Broker



client.subscribe((“data/test”,qos=1))

client.publish(topic="TestingTopic", payload="TestingPayload", qos=1, retain=False)

#todo continue with on_message

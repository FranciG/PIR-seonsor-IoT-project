Import paho.mqtt.client as mqtt

ourClient = mqtt.Client(“makerio_mqtt”)     # Create a MQTT client object
ourClient.connect(“test.mosquitto.org”, 1883)       # Connect to the test MQTT broker. Config takes up to 4 parameters including the host, port, keep alive, and bind address, but we only need to provide the host IP.

# publish(topic, message)

ourClient.publish(“AC_unit”, “on”)          # Turn the AC unit on

#source: https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi
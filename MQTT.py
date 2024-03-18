import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code and also haveing connection status non-secuered {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1993, 60) 


client.publish("test", "Message")
time.sleep(5)

client.disconnect() #stop the mqtt client
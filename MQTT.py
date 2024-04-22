import random
import time
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, broker, port):
        self.client_id = "MAIN"
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code:", rc)

    def on_message(self, client, userdata, message):
        print("Received message:", str(message.payload.decode("utf-8")))

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)
    
    def publish_loop(self , topic , msg , times):
        for i in range(times):
            k = msg
            self.publish(topic=topic, message=msg)
            print(f"published {k}")
            time.sleep(10)            



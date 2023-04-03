import paho.mqtt.client as mqtt
import time

def publishMessageOnTopic(message,topic):
    mqttBroker="mqtt.eclipseprojects.io"
    client=mqtt.Client("Télecommande")
    client.connect(mqttBroker)
    client.publish(topic,message)




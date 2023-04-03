import paho.mqtt.client as mqtt
import time
import RobotMove as control


def on_message(client, useradata, message):
    ecoded_message = str(message.payload.decode("utf-8"))
    print("received message : ", str(message.payload.decode("utf-8")))
    client.data=ecoded_message
    
    
   
    
mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Robot")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("Walt/mouvement")
client.data=" "
client.on_message = on_message


stop=False
if(client.data!=" "):
    stop = False
else :
    if(client.data=="STOP"):
        control.stop()
    else :
        stop=True

while stop:
    control.move(client.data)
    time.sleep(0.1)
    
client.loop_end()
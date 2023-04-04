import paho.mqtt.client as mqtt
import time
import RobotMove as control
import ControlDcServo as servo

def on_message(client, useradata, message):
    ecoded_message = str(message.payload.decode("utf-8"))
    #print("received message : ", str(message.payload.decode("utf-8")))
    client.data=ecoded_message
    
    
   
channel12value=150
channel13value=150
channel14value=150
channel15value=160

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Robot")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("Walt/mouvement")
client.data=""
client.on_message = on_message
direction="forward"

while True:
    if(client.data=="UP" or client.data=="RIGHT" or client.data=="LEFT"):
        print("hello",client.data)
        control.move(60, direction, client.data, radius=0.6)
        pass
    if(client.data=="forward" or direction=="backward"):
         direction=client.data
    if(client.data=="CHANNEL12UP"):
         channel12value=servo.moveServo(12,"UP",channel12value)
    if(client.data=="CHANNEL12DOWN"):
         channel12value=servo.moveServo(12,"DOWN",channel12value)


    if(client.data=="CHANNEL13UP"):
         channel13value=servo.moveServo(13,"UP",channel13value)
    if(client.data=="CHANNEL13DOWN"):
         channel13value=servo.moveServo(13,"DOWN",channel13value)

    if(client.data=="CHANNEL14UP"):
         channel14value=servo.moveServo(14,"UP",channel14value)
    if(client.data=="CHANNEL14DOWN"):
         channel14value=servo.moveServo(14,"DOWN",channel14value)

    if(client.data=="CHANNEL15UP"):
         channel15value=servo.moveServo(15,"UP",channel15value)
    if(client.data=="CHANNEL15DOWN"):
         channel15value=servo.moveServo(15,"DOWN",channel15value)    
               
    if(client.data=="STOP"):
            control.stop()
            pass
    time.sleep(0.1)
    
client.loop_end()

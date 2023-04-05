import paho.mqtt.client as mqtt
import time
import RobotMove as control
import ControlDcServo as servo
import infra as infra
import uuid
import socket 
import imageProcess as image
def on_message(client, useradata, message):
    ecoded_message = str(message.payload.decode("utf-8"))
    print("received message : ", str(message.payload.decode("utf-8")))
    client.data=ecoded_message
    
    
remote_address = "172.18.83.101"
remote_port = 12345

# Create a UDP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

channel12value=150
channel13value=150
channel14value=150
channel15value=160
enter=False

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Robot")


client.connect(mqttBroker)
infra.setup(client)
direction="forward"
client.loop_start()
client.subscribe("Walt/mouvement")
client.data=""
client.on_message = on_message


while True:
    print(direction)
    if(client.data=="UP" or client.data=="right" or client.data=="left"):
        print("hello",client.data)
        control.moveWIthMessageInput(client.data,direction)
        pass
    if(client.data=="forward" or client.data=="backward"):
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
    if(client.data=="PHOTO"):
         socket.sendto(image.CaptureImage.encode("utf-8"), (remote_address, remote_port))
    if(client.data=="TIR"):
         infra.tir(uuid.getnode())
     
    time.sleep(0.1)
    
client.loop_end()
socket.close()

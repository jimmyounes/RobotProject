import InfraLib
import RPi.GPIO as GPIO

def tir(tankID):
    InfraLib.IRBlast(tankID, "LASER")
def reception(client):
    IR_RECEIVER = 15
    GPIO.setup(IR_RECEIVER, GPIO.IN)
    GPIO.add_event_detect(IR_RECEIVER, GPIO.FAILLING, callback=lambda x: InfraLib.getSignal(IR_RECEIVER, client), bouncetime=100)

LINE_PIN_MIDDLE = 36


def enterFlagArea(client,tankID,enter):
  if GPIO.input(LINE_PIN_MIDDLE) == GPIO.LOW and enter==False:
    enter=True
    client.publish("tanks/"+hex(tankID)+"/flag","ENTER_FLAG_AREA")
  else:
    if(enter==True):
        enter=False
        client.publish("tanks/"+hex(tankID)+"/flag","EXIT_FLAG_AREA")    
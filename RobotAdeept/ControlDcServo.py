#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Servos
# Author      : William
# Date        : 2019/02/23
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys



def moveServo(channel,value,direction):
	if(direction=="UP"):
		value=value+10
	else:
		value=value-10
	pwm.set_pwm(channel, 0, value)
	return value	

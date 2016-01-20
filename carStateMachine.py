#!/usr/bin/env python

# dependencies:
# pip install transitions
# or from https://github.com/tyarkoni/transitions

from transitions import Machine

import os
import time

def beep(beeps):
	os.system ("wget 192.168.0.1/beep%d -O ignitionTime.txt --quiet" %beeps)

def CarDetected():
	response = os.system("ping -c 1 192.168.0.1 > /dev/null 2>&1")
	if response == 0:
		return True
	return False

def CarNotDetected():
	response = os.system("ping -c 3 192.168.0.1 > /dev/null 2>&1")
	if response == 0:
		return False
	return True

def departTasks():
	pass

def arrivalTasks():
	pass

def ignitionTime():
	os.system("wget 192.168.0.1 -O ignitionTime.txt --quiet")
	with open('ignitionTime.txt', 'r') as file:
		ignitionTime = file.read()
	file.close()
	return ignitionTime

# Statemachine:

class Car(object):
    def on_enter_waitingForCar(self): 
		print ("Entered state waitingForCar")

    def on_enter_getIgnitionTime(self): 
		print ("Entered state getIgnitionTime")

    def on_enter_departTasks(self): 
		print ("Entered state departTasks")

    def on_enter_arrivalTasks(self): 
		print ("Entered state arrivalTasks")

    def on_enter_waitForNoCar(self): 
		print ("Entered state waitForNoCar")



stevesCar = Car()

states=['waitingForCar', 'getIgnitionTime', 'departTasks', 'arrivalTasks', 'waitForNoCar']

transitions = [
    { 'trigger': 'detected', 'source': 'waitingForCar', 'dest': 'getIgnitionTime' },
    { 'trigger': 'error', 'source': 'getIgnitionTime', 'dest': 'waitingForCar' },
    { 'trigger': 'shorttime', 'source': 'getIgnitionTime', 'dest': 'departTasks' },
    { 'trigger': 'longtime', 'source': 'getIgnitionTime', 'dest': 'arrivalTasks' },
    { 'trigger': 'notdetected', 'source': 'waitForNoCar', 'dest': 'waitingForCar' },
    { 'trigger': 'advance', 'source': 'departTasks', 'dest': 'waitForNoCar' },
    { 'trigger': 'advance', 'source': 'arrivalTasks', 'dest': 'waitForNoCar' }
]

machine = Machine(stevesCar, states=states, transitions=transitions, initial='waitingForCar')

while(1):

	if stevesCar.state == 'waitingForCar':	
		if CarDetected():
			stevesCar.detected()
		else:
			time.sleep(5)

	elif stevesCar.state == 'getIgnitionTime':
		try:
			if int(ignitionTime()) < 180:
				stevesCar.shorttime()
			else:
				stevesCar.longtime()
		except:
			stevesCar.error()

	elif stevesCar.state == 'departTasks':
		departTasks()
		stevesCar.advance()

	elif stevesCar.state == 'arrivalTasks':
		arrivalTasks()
		stevesCar.advance()

	elif stevesCar.state == 'waitForNoCar':
		if CarNotDetected():
			stevesCar.notdetected()
		else:
			time.sleep(5)



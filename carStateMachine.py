#!/usr/bin/env python

# dependencies:
# pip install transitions
# or from https://github.com/tyarkoni/transitions

from transitions import Machine

import os
import time
import datetime

# Statemachine:

class CarDetector(object):

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

	def __init__(self, name, IPAddress):
		self.name = name
		self.IPAddress = IPAddress
		self.machine = Machine(self, states=CarDetector.states, transitions=CarDetector.transitions)

	def on_enter_waitingForCar(self):
		self.printMessage()
		while(not self.CarDetected()):
			time.sleep(5)
		self.detected()

	def on_enter_getIgnitionTime(self):
		self.printMessage()
		try:
			if int(self.ignitionTime()) < 30:
				self.shorttime()
			else:
				self.longtime()
		except:
			self.error()

	def on_enter_departTasks(self):
		self.printMessage()
		self.departTasks()
		self.advance()

	def on_enter_arrivalTasks(self):
		self.printMessage()
		self.arrivalTasks()
		self.advance()

	def on_enter_waitForNoCar(self):
		self.printMessage()
		while(not self.CarNotDetected()):
			time.sleep(5)
		self.notdetected()

	def printMessage(self):
		print(self.name),
		print("entered state %s" %self.state),
		print(datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y'))

	def CarDetected(self):
		response = os.system("ping -c 1 %s > /dev/null 2>&1" %self.IPAddress)
		if response == 0:
			return True
		return False

	def ignitionTime(self):
		os.system("wget %s -O %s_ignitionTime.txt --quiet" %(self.IPAddress, self.name))
		with open("%s_ignitionTime.txt" %self.name, 'r') as file:
			ignitionTime = file.read()
		file.close()
		print(self.name),
		print("ignition time is %s seconds" %ignitionTime)
		return ignitionTime

	def departTasks(self):
		self.beep(2);

	def arrivalTasks(self):
		self.beep(3);

	def beep(self, beeps):
		os.system ("wget %s/beep%d -O %s_ignitionTime.txt --quiet" %(self.IPAddress, beeps, self.name))

	def CarNotDetected(self):
		response = os.system("ping -c 3 %s > /dev/null 2>&1" %self.IPAddress)
		if response == 0:
			return False
		return True


# Create an object and kick the state machine into life

stevesCar = CarDetector("stevesCar", "192.168.0.1")
stevesCar.to_waitingForCar() # forces calling on_enter_waitingForCar

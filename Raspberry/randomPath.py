from ActorControl import *
import time
import random

actorControl = ActorControl()
motorControl = actorControl.getMotor()

def rotate(direction):
	#direction *= -1
	if direction > 0: # links
		for i in range(abs(direction)):
			motorControl.set([1, 0], 0.9, 50)
	elif direction < 0: # rechts
		for i in range(abs(direction)):
			motorControl.set([0, 1], 0.8, 50)

def drive(direction):
	#direction *= -1
	if direction > 0:
		for i in range(abs(direction)):
			motorControl.set([1, 1], 1.6, 100)
	elif direction < 0:
		for i in range(abs(direction)):
			motorControl.set([0, 0], 0.7, 100)

def e():
	while True:
		mode = int(random.random() * 2)
		drive(1)
		if mode == 0:
			rotate(-1)
		else:
			rotate(1)
#		drive(-1)

def block(speed, rotation):
	drive(speed)
	drive(-1)
	rotate(rotation)

def f():
	block(2, 1)
	block(2, 1)
	block(2, -1)
	block(2, 1)
	block(2, -1)
	block(7, -1)

def d():
	while True:
		for i in range(5):
			for j in range(2):
				block(2, 1)
			block(2, -1)
			block(2, 1)
		block(2, -1)

def c():
	for i in range(10):
		drive(1)
		drive(-1)

def b():
	for i in range(10):
		rotate(1)
		rotate(-1)

def a():
	for i in range(50):
		drive(3)
		drive(-1)
		rotate(1)
		drive(3)
		drive(-1)
		rotate(1)
		drive(3)
		drive(-1)
		rotate(-1)

f()

from ActorControl import *
import time

actorControl = ActorControl()
motorControl = actorControl.getMotor()

def rotate(direction):
	if direction == 1:
		motorControl.set([1, 0], 0.9, 50)
	elif direction == -1:
		motorControl.set([0, 1], 0.9, 50)

def drive(direction):
	if direction == 1:
		motorControl.set([1, 1], 1, 100)
	elif direction == -1:
		motorControl.set([0, 0], 1, 100)

for i in range(20):
	drive(1)
	drive(1)
	rotate(1)
	drive(-1)
	drive(1)
	drive(1)
	rotate(1)
	drive(-1)
	drive(1)
	drive(1)
	rotate(-1)
	drive(-1)
#print "driving forward"
#	motorControl.set([1,1],2.7,100) # forward
#	motorControl.set([1,0],2.5,100) # left
#	motorControl.set([0,0],2.5,100) # backward
'''print "driving backward"
motorControl.set([0,0],0.7,100)
print "rotate"
motorControl.set([1,0],0.9,50)
print "forward"
motorControl.set([1,1],1.5,100)
print "rotate"
motorControl.set([1,0],0.9,50)
print "forward"
motorControl.set([1,1],2,100)
print "rotate"
motorControl.set([0,1],0.9,50)
print "forward"
motorControl.set([1,1],1,100)
print "backward"
motorControl.set([0,0],1,100)
'''

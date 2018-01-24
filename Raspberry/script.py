#!/bin/python

from searchArduinos import Arduinos
from ActorControl import *
#from Navigation import Map

'''
sftp pi@192.168.43.189
put local remote
get remote local

put ./Raspy.py ./script.py
'''

actorControl = ActorControl()
motorControl = actorControl.getMotor()

#motorControl = Motor()
while True:
    motorControl.play()
'''
names = {'i2c': 'sensor', 'us': 'ultrasonic'}
arduinos = Arduinos(names)
arduinos.checkArduinoExistence(names)

temp = arduinos.getValues('Temp')
distances = arduinos.getValues('Distances', 'us')
motorControl.set(1)
'''
'''
map = Map()
map.setField(0, 0, 0, [False, True, True, True])
print(map.getSize())
map.setField(0, 1, 1, [])
print(map.getSize())
print(map.getField(0, 0))

print(map.getValidNeighbours(0, 0))
print(map.size)
'''
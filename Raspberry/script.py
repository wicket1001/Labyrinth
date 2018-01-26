#!/usr/bin/python
# coding=utf-8

from searchArduinos import Arduinos
#from ActorControl import *
from Navigation import Map
import os

'''
sftp pi@192.168.43.189
put local remote
get remote local

put ./Mazerobot/Raspy.py ./script.py
'''

def motorTest():
    actorControl = ActorControl()
    motorControl = actorControl.getMotor()

    motorControl = Motor()
    motorControl.set(1)
    while True:
        motorControl.play()

def arduinoConnectionTest():
    names = {'i2c': 'sensor', 'us': 'ultrasonic'}
    arduinos = Arduinos(names)
    arduinos.checkArduinoExistence(names)
    while True:
        input = raw_input("Direct Serial")
        arduinos.write(input, 'us')

    '''
    names = {'i2c': 'sensor', 'us': 'ultrasonic'}
    arduinos = Arduinos(names)
    arduinos.checkArduinoExistence(names)

    temp = arduinos.getValues('Temp')
    distances = arduinos.getValues('Distances', 'us')
    '''

#def drivePath

def solveMaze(map, startCoordinates, correct, dy, goalCoordinates = None):
    currentCoordinates = startCoordinates
    cost = 0
    goalField = None
    if goalCoordinates is not None:
        goalField = map.getField(goalCoordinates[0], goalCoordinates[1])
    currentField = None
    while goalCoordinates is None or map.getPath(map.getField(currentCoordinates[0], currentCoordinates[1]), goalField) is None:
        currentField = map.getField(currentCoordinates[0], currentCoordinates[1])

        shortestDistance = 1000
        shortestPath = None
        unknownFields = map.getAllUnknownFields()
        for unknownField in unknownFields:
            path = map.getPath(currentField, unknownField)
            if path and len(path) < shortestDistance:
                shortestDistance, shortestPath = len(path), path
        for unknownField in unknownFields:
            coords = unknownField.getCoordinates()
            map.removeField(coords[0], coords[1])
        # TODO DRIVE TO GOAL
        if shortestPath is None:
            break
        currentField = shortestPath[len(shortestPath) - 1]
        # TODO MEASURE FIELD <
        currentCoordinates = currentField.getCoordinates()
        correctCoordinates = (currentCoordinates[0] + dx, currentCoordinates[1] + dy)
        correctField = correct.getField(correctCoordinates[0], correctCoordinates[1])
        # TODO END >
        correctWalls = [True] * 4
        for i in range(4):
            correctWalls[i] = correctField.isWall(i)
        map.setField(currentCoordinates[0], currentCoordinates[1], correctWalls)
        raw_input("Next: ")

        os.system("clear")
        cost += len(shortestPath) - 1
        print(cost)

        print(map.drawPath(shortestPath))
    print(cost)
    if goalField is None:
        goalField = map.getField(startCoordinates[0], startCoordinates[1])
    raw_input("Fin: ")
    wayToGoal = map.getPath(currentField, goalField)
    print(map.drawPath(wayToGoal))

    return cost

def mapTest():
    # TODO rotate that longest distance is in front

    file = "/home/user/Schreibtisch/python_Projects/Mazerobot/map1.txt"
    correct1 = Map(file)

    file = "/home/user/Schreibtisch/python_Projects/Mazerobot/map2.txt"
    correct2 = Map(file)

    map1 = Map()
    startCoordinates = [10, 10]

    startWalls = [True] * 4 # TODO Input by robot
    rot = 2
    startWalls[rot] = False
    map1.setField(startCoordinates[0], startCoordinates[1], startWalls)
    startField = map1.getField(startCoordinates[0], startCoordinates[1])

    goalWalls = [True] * 4
    goalWalls[rot] = False
    goalCoordinates = [startCoordinates[0] + 6, startCoordinates[1] + 1]
    map1.setField(goalCoordinates[0], goalCoordinates[1], goalWalls)
    goalField = map1.getField(goalCoordinates[0], goalCoordinates[1])

    cost = 0
    cost += solveMaze(map1, startCoordinates, correct1, -7, goalCoordinates)
    # TODO FAHRE NACH OBEN

    map2 = Map()
    startWalls = [True] * 4
    rot = 2
    startWalls[rot] = False
    map2.setField(startCoordinates[0], startCoordinates[1], startWalls)
    cost += solveMaze(map2, startCoordinates, correct2, -6)
    print(cost)

'''
    map = Map(file)
    print(map)

    path = map.getPath(map.getField(1, 1), map.getField(2, 2))
    if path is None:
        print("No valid Path found!")
    else:
        print(map.drawPath(path))
'''


dx = -10

#motorTest()
#arduinoConnectionTest()
mapTest()



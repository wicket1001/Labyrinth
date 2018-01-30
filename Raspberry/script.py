#!/usr/bin/python
# coding=utf-8

from searchArduinos import Arduinos
from ActorControl import *
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
    print(actorControl)
    global motorControl
    motorControl = actorControl.getMotor()

    while True:
        motorControl.play()

def arduinoConnectionTest():
    names = {'i2c': 'sensor', 'us': 'ultrasonic'}
    arduinos = Arduinos(names)
    arduinos.checkArduinoExistence(names)
    while True:
        input = raw_input("Direct Serial")
        arduinos.write(input, 'us')

def solveMaze(map, startCoordinates, rot, correct, dx, dy, goalCoordinates = None):
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
        currentCoordinates = currentField.getCoordinates()
        # TODO MEASURE FIELD <
        #print currentCoordinates[0]
        correctCoordinates = (currentCoordinates[0] + dx, currentCoordinates[1] + dy)
        correctField = correct.getField(correctCoordinates[0], correctCoordinates[1])
        # TODO END >
        correctWalls = [True] * 4
        for i in range(4):
            correctWalls[i] = correctField.isWall(i)
        map.setField(currentCoordinates[0], currentCoordinates[1], correctWalls)

        os.system("clear")
        cost += len(shortestPath) - 1
        print(cost)

        for i in range(len(shortestPath) - 1):
            s = shortestPath[i].getCoordinates()
            e = shortestPath[i + 1].getCoordinates()
            getRotationDifference(s[0], s[1], rot, e[0], e[1])
        print "\n"
    print(cost)
    if goalField is None:
        goalField = map.getField(startCoordinates[0], startCoordinates[1])
    wayToGoal = map.getPath(currentField, goalField)
    for i in range(len(wayToGoal) - 1):
        s = shortestPath[i].getCoordinates()
        e = shortestPath[i + 1].getCoordinates()
        getRotationDifference(s[0], s[1], rot, e[0], e[1])
    print wayToGoal

    return cost

def rotate(direction):
    global motorControl
    if direction > 0: # links
        for i in range(abs(direction)):
            motorControl.set([0, 1], 0.9, 50)
    elif direction < 0:
        for i in range(abs(direction)):
            motorControl.set([1, 0], 0.9, 50)


def drive(direction):
    global motorControl
    if direction == 1:
        motorControl.set([1, 1], 0.7, 100)
    elif direction == -1:
        motorControl.set([0, 0], 0.7, 100)


def getRotationDifference(sx, sy, rot, ex, ey):
    print(sx, sy, rot, ex, ey)
    dx = sx - ex
    dy = sy - ey
    if rot % 2 == 0 : # y veränderung -> 0
        if dx == 0:
            if dy < 0:
                rotate(2)
        else: # dx verändert
            if dx > 0:
                rotate(-1)
            else: # dx < 0
                rotate(1)
    else:  # x veränderung -> 0
        if dy == 0:
            if dx < 0:
                rotate(2)
        else:
            if dy > 0:
                rotate(-1)
            else:
                rotate(1)

    drot = 0
    print drot
    rotate(drot)

def mapTest():
    # TODO rotate that longest distance is in front

    file = "./map1.txt"
    correct1 = Map(file)

    file = "./map2.txt"
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
    cost += solveMaze(map1, startCoordinates, rot, correct1, -1, -7, goalCoordinates)
    # TODO FAHRE NACH OBEN

    global motorControl
    rotate(-1)
    drive(5)

    map2 = Map()
    startWalls = [True] * 4
    rot = 2
    startWalls[rot] = False
    map2.setField(startCoordinates[0], startCoordinates[1], startWalls)
    cost += solveMaze(map2, startCoordinates, rot, correct2, -10, -6)
    print(cost)

motorControl = None
motorTest()
#arduinoConnectionTest()
mapTest()
#motorTest()


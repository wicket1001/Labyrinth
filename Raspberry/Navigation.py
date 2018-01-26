# coding=utf-8
import math

class Field:
    x = 0
    y = 0
    walls = None

    def __init__(self, x, y, walls=None):
        if walls is None:
            walls = [True, True, True, True]
        self.x = x
        self.y = y
        self.walls = walls

    def getCoordinates(self):
        return self.x, self.y

    def getWalls(self):
        return self.walls

    def isWall(self, orientation):
        return self.walls[orientation]

    def __str__(self):
        return "Field[" + str(self.x) + ", " + str(self.y) + \
               "] with " + str(self.walls) + " walls."

class Map:
    size = 21

    def __init__(self, filename=None):
        self.map = []
        for y in range(self.size):
            self.map.append([])
            for x in range(self.size):
                self.map[y].append(None)
        if filename is not None:
            file = open(filename, "r")
            lines = file.readlines()
            wallsT = []
            wallsS = []
            wallsB = []
            num = 0
            for line in lines:
                if num % 2 == 0:
                    wallsT = wallsB
                    wallsB = []
                line = line.strip()
                chnum = 0
                for ch in line:
                    if num % 2 == 0:
                        if chnum % 2 == 1 and ch != ' ':
                            wallsB.append(True)
                        elif chnum % 2 == 1:
                            wallsB.append(False)
                    else:
                        if chnum % 2 == 0 and ch != ' ':
                            wallsS.append(True)
                        elif chnum % 2 == 0:
                            wallsS.append(False)
                    chnum += 1
                if num % 2 == 0 and num >= 2:
                    #print(wallsT, wallsS, wallsB)
                    for i in range(len(wallsT)):
                        self.setField(i, num/2-1, [wallsB[i], wallsS[i+1], wallsT[i], wallsS[i]])
                    wallsT = []
                    wallsS = []
                num += 1

    def drawPath(self, fields):
        return self.__str__(fields)

    def __str__(self, fields=None):
        if fields is None:
            fields = []
        mapStr = ""
        for y in range(len(self.map)):
            l1 = ""
            l2 = ""
            l3 = ""
            for x in range(len(self.map[y])):
                f = self.getField(x, y)
                l1 += "+"
                if f is not None and f.isWall(2) or self.getField(x, y-1) and self.getField(x, y-1).isWall(0):
                    l1 += "---"
                else:
                    l1 += "   "
                if f is not None and f.isWall(3) or self.getField(x-1, y) and self.getField(x-1, y).isWall(1):
                    l2 += "|"
                else:
                    l2 += " "
                l2 += " " #str(x) + str(y)
                if f in fields:
                    l2 += "•"
                else:
                    l2 += " "
                l2 += " "
                if x == len(self.map[y]):
                    if f is not None and f.isWall(1):
                        l2 += "|"
                if y == len(self.map)-1:
                    if f is not None and f.isWall(2):
                        l3 += "+---"
                    else:
                        l3 += "+   "
            if y == len(self.map)-1:
                l3 += "+\n"
            mapStr += l1+"+\n"+l2+"\n"+l3
        return mapStr

    def getField(self, x, y):
        return len(self.map) > y >= 0 and len(self.map[y]) > x >= 0 and self.map[y][x] or None

    def setField(self, x, y, walls=None):
        self.map[y][x] = Field(x, y, walls)

    def removeField(self, x, y):
        self.map[y][x] = None

    def getSize(self):
        return len(self.map), len(self.map[0])

    def getValidNeighbours(self, x, y):
        neighbours = {}
        this = self.getField(x, y)
        #  x  y rot
        #  0  1 0
        #  1  0 1
        #  0 -1 2
        # -1  0 3
        for rot in range(4):
            dx = (rot % 2 == 1 and 1 or 0) * ((rot >= 2) and -1 or 1)
            dy = (rot % 2 == 0 and 1 or 0) * ((rot >= 2) and -1 or 1)
            if 0 <= x + dx < self.size and 0 <= y + dy < self.size and self.getField(x + dx, y + dy) is not None:
                if not this.isWall(rot):
                    neighbours[rot] = self.getField(x + dx, y + dy)
                else:
                    neighbours[rot] = None
        return neighbours

    def getAllNeighbours(self, x, y):
        neighbours = {}
        this = self.getField(x, y)
        for rot in range(4):
            dx = (rot % 2 == 1 and 1 or 0) * ((rot >= 2) and -1 or 1)
            dy = (rot % 2 == 0 and 1 or 0) * ((rot >= 2) and -1 or 1)
            if 0 <= x + dx < self.size and 0 <= y + dy < self.size and not this.isWall(rot):
                if self.getField(x + dx, y + dy) is not None:
                    neighbours[rot] = self.getField(x + dx, y + dy)
                else:
                    neighbours[rot] = None
        return neighbours

    def getPath(self, start, end): # field
        def getQueueIndex(obj):
            return obj["dist"]
        queue = [{"field": start, "dist": 0, "via": None}]
        while queue[0]["field"] is not end:
            current = queue[0]
            coordinates = current["field"].getCoordinates()
            neighbours = self.getValidNeighbours(coordinates[0], coordinates[1]) # {0: field, 1: field}
            for index in neighbours.keys():
                neighbour = neighbours.get(index)
                if neighbour is not current["via"] and neighbour is not None:
                    queueIndex = None
                    for i in range(len(queue)):
                        q = queue[i]
                        if q["field"] is neighbour:
                            queueIndex = i
                            break
                    if queueIndex is None:
                        queue.append({"field": neighbour, "dist": current["dist"] + 1, "via": current})
                    else:
                        queue[queueIndex]["via"] = current
                        queue[queueIndex]["dist"] += 1
                    # Add Rotation Time (opt.)
            queue.pop(0)
            queue.sort(key=getQueueIndex)
            if len(queue) == 0 or queue[0]["dist"] >= self.size * self.size:
                return None
        path = [queue[0]]
        while path[0] is not start and path[0]["via"] is not None:
            path.insert(0, path[0]["via"])
        out = []
        for i in range(len(path)):
            out.append(path[i]["field"])
        return out

    def getDistance(self, (startX, startY), (endX, endY)):
        dx = startX - endX
        dy = startY - endY
        return math.sqrt(dx * dx + dy * dy)

    def getAllUnknownFields(self):
        fields = []
        for y in range(self.size):
            for x in range(self.size):
                if self.map[y][x] is not None:
                    neighbours = self.getAllNeighbours(x, y)
                    for i in neighbours.keys(): # fully discovered, partially discoverd, no d at all
                        if neighbours[i] is None: # dann self.map[x][y] verbindung zu neighbour
                            dx = (i % 2 == 1 and 1 or 0) * ((i >= 2) and -1 or 1)
                            dy = (i % 2 == 0 and 1 or 0) * ((i >= 2) and -1 or 1)

                            walls = [True] * 4
                            walls[(i + 2) % 4] = False
                            newField = Field(x + dx, y + dy, walls)
                            fields.append(newField)
                            #self.map[y + dy][x + dx] = None
                            self.map[y + dy][x + dx] = newField
        return fields





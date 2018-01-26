import serial
import time

class Arduinos:
    arduinos = {}

    def __init__(self, names):
        self.names = names
        import serial.tools.list_ports_linux as listPorts
        ports = listPorts.comports()

        for p in ports:
            if p[2] != 'n/a':
                found = False
                ser = serial.Serial(p[0])
                time.sleep(2)
                ser.write("name")
                for i in range(1000):
                    time.sleep(0.01)
                    if ser.inWaiting():
                        # print "inWaiting"
                        numBytes = ser.inWaiting()
                        inputBytes = ser.read(numBytes)
                        found = True
                        break
                if found:
                    self.arduinos[inputBytes] = serial.Serial(p[0])

    def __del__(self):
        for key in self.arduinos.keys():
            if self.exists(key):
                self.resetArduino(key)

    def resetArduino(self, key):
        inputBytes = ""
        arduino = self.arduinos[key]
        if self.exists(key):
            arduino.write("reset")
            numBytes = arduino.inWaiting()
            inputBytes = str(arduino.read(numBytes))
            print "Reset " + str(inputBytes)
        return inputBytes == "done"

    def setValue(self, field, value, index="i2c"):
        name = self.names[index]
        arduino = self.arduinos[name]
        arduino.write(">set" + field + ":" + str(value))
        while True:
            time.sleep(0.01)
            if arduino.inWaiting():
                try:
                    numBytes = arduino.inWaiting()
                    answer = arduino.read(numBytes).split(':')
                    return int(answer[0] == value)
                except:
                    print(name + " arduino did not answer correct")
                    return False

    def getValues(self, field, index="i2c", decimal=False):
        name = self.names[index]
        arduino = self.arduinos[name]
        arduino.write(">get" + field)
        while True:
            time.sleep(0.01)
            if arduino.inWaiting():
                try:
                    numBytes = arduino.inWaiting()
                    answer = arduino.read(numBytes).split(',')
                    array = []
                    for field in answer:
                        if decimal:
                            array.append(int(field))
                        else:
                            array.append(float(field))
                    return array
                except:
                    print name + " arduino did not respond the correct value for " + field
                    return [0, 0, 0]

    def write(self, text, index="i2c"):
        name = self.names[index]
        arduino = self.arduinos[name]
        arduino.write(text)

    def inWaiting(self, key):
        if self.exists(key):
            return self.arduinos[key].inWaiting()

    def read(self, key, size = 2):
        if self.exists(key):
            return self.arduinos[key].read(size)

    def checkArduinoExistence(self, keys):
        available = True
        for key in keys:
            if not self.exists(key):
                print("Arduino " + key + " is not available.")
                available = False
        if not available:
            raise ImportError("An arduino is not available.")
        else:
            print(self.keys())

    def exists(self, key):
        return key in self.arduinos.keys()

    def keys(self):
        return self.arduinos.keys()

    def __len__(self):
        return len(self.arduinos)


import serial
import time

def getPorts():
    arduinos = []
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
                arduinos.append(serial.Serial(p[0]))

    print(arduinos)

#getPorts()

def simple():
    import serial.tools as listPorts
    s = serial.Serial('/dev/ttyS0', 9600)
    print(s)
    if s.isOpen() == False:
        s.open()
    time.sleep(5)
    print("Es")

#    if p[2] != 'n/a':
#                found = False
#                ser = serial.Serial(p[0])
#                time.sleep(2)

    s.write(">setColor:1")
    print("Write")
    try:
        while True:
            userinput = raw_input("Write: ")
            s.write(userinput)
            response = s.readline()
            print(response)
    except KeyboardInterrupt:
        s.close()

<<<<<<< HEAD:Raspberry/Serial.py
=======
#getPorts()
>>>>>>> 3f725725381712246a3fe376c15de571b564da04:Raspberry/Test.py
simple()

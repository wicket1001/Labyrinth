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
    #import serial.tools as listPorts
    # p = listPorts.comports()
    #print(p)
    s = serial.Serial('/dev/ttyAMA0', 9600)
    print(s)
    if s.isOpen() == False:
        s.open()
    time.sleep(5)
    print("Established")

#    if p[2] != 'n/a':
#                found = False
#                ser = serial.Serial(p[0])
#                time.sleep(2)

    #s.write(">setColor:1\n")
    #respone = s.readline()
    #print(respone)
    try:
        while True:
            userinput = raw_input("Write: ")
            s.write(userinput)
            response = s.readline()
            print("Respone: ", response)
    except:
        s.close()


simple()

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
    s = serial.Serial('/dev/tty1', 9600)  # Namen ggf. anpassen
    s.open()
    time.sleep(5)  # der Arduino resettet nach einer Seriellen Verbindung, daher muss kurz gewartet werden

    s.write(">setColor:1")
    try:
        while True:
            response = s.readline()
            print(response)
    except KeyboardInterrupt:
        s.close()

simple()

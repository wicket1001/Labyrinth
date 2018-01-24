import RPi.GPIO as GPIO
import re
import time

class ActorControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.motor = Motor()
        self.button = Button()

    def getMotor(self):
        return self.motor

    def getButton(self):
        return self.button

    def __del__(self):
        GPIO.cleanup()


class Motor:
    blank = re.compile(r"\s")
    quit = re.compile(r"q.*")
    stop_regex = re.compile(r"s.*")

    motors = [  [10, 9],  # r
                [25, 8]] # l

    encoder = [[17, 27],
               [22, 23]]

    enables = [12, 13]  # r, l

    #for motor in motors:
    direction = [   (GPIO.HIGH, GPIO.LOW),
                    (GPIO.LOW, GPIO.HIGH)]
    names = ["backward", "forward"]

    def __init__(self):
        for motor in self.motors:
            for pin in motor:
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        for pin in self.enables:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        hertz = 50

        self.enables[0] = GPIO.PWM(self.enables[0], hertz)
        self.enables[1] = GPIO.PWM(self.enables[1], hertz)

    def set(self, direction, sleeps=-1, speed=100):
        for motor in self.motors:
            GPIO.output(motor, self.direction[direction])

        for pin in self.enables:
            pin.start(speed)

        if sleeps != -1:
            time.sleep(sleeps)
            self.stop()

    def stop(self):
        self.set(1, speed=0)

    def play(self):
        print("Config [direction=0/1], [time], [speed=0-100], []")
        user_input = raw_input("Start: ")
        print(user_input) # TODO: stop on empty
        if user_input == '' or self.quit.match(user_input):
            exit(0)

        elif self.stop_regex.match(user_input):
            self.stop()

        else:
            user_input = self.blank.sub("", user_input)

            inputs = user_input.split(",")
            for i in range(len(inputs)):
                inputs[i] = int(inputs[i])

            if len(inputs) == 1:
                self.set(inputs[0])
            elif len(inputs) == 2:
                self.set(inputs[0], inputs[1])
            elif len(inputs) == 3:
                self.set(inputs[0], inputs[1], inputs[2])


class Button:
    pin = 24
    pressed = False

    def __init__(self):
        GPIO.setup(self.pin,
                   GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.pin,
                              GPIO.FALLING,
                              callback=self.callback,
                              bouncetime=300)

    def waitForStart(self):
        GPIO.wait_for_edge(pin, GPIO.FALLING)

    def callback(self):
        pressed = True
        print("Interrupt callback")

    def getPressed(self):
        if self.pressed:
            pressed = False
            return True
        else:
            return False


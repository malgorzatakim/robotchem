import serial
from time import sleep

class Platform:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyACM0', 9600)
        #pass

    def moveUp(self, steps):
        print "Moving up by: {} steps".format(steps)
        for _ in range(steps):
            #msg = "0"
            #pass
            self.serial.write("1")
            #while msg != "1\n":
             #   msg = self.serial.readline()
            #print msg
            sleep(0.1)
            #self.serial.read(self.serial.inWaiting())
            #add read inside the loops

    def moveDown(self, steps):
        print "Moving down by: {} steps".format(steps)
        for _ in range(steps):
            #msg = "0"
            #pass
            self.serial.write("2")
            #while msg != "1\n":
            #    msg = self.serial.readline()
            #    print msg
            sleep(0.1)
            #self.serial.read(self.serial.inWaiting())

    def moveDownAll(self):
        #msg = "0"
        self.serial.write("4")
        #while msg != "1\n":
        #    msg = self.serial.readline()
        #self.serial.read(self.serial.inWaiting())
        sleep(40)
        #pass
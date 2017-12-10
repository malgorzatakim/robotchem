import serial

class Platform:
    def __init__(self):
        #self.serial = serial.Serial('/dev/ttyACM0', 9600)
        pass

    def moveUp(self, steps):
        print "Moving up by: {} steps".format(steps)
        for _ in range(steps):
            pass
            #self.serial.write(1)
            #add read inside the loop

    def moveDown(self, steps):
        print "Moving down by: {} steps".format(steps)
        for _ in range(steps):
            pass
            #self.serial.write(2)

    def moveDownAll(self):
        pass

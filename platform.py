import serial

class Platform:
    def __init__(self):
        #self.serial = serial.Serial('/dev/ttyACM0', 9600)
        pass

    def moveUp(self, steps):
        print "Moving up by: {} steps".format(steps)
        for _ in range(steps):
            #self.serial.write(1)
            #ser.read(ser.inWaiting())
            #add read inside the loop

    def moveDown(self, steps):
        print "Moving down by: {} steps".format(steps)
        for _ in range(steps):
            pass
            #self.serial.write(2)
            #ser.read(ser.inWaiting())

    def moveDownAll(self):
        #self.serial.write(4)
        #ser.read(ser.inWaiting())
        pass

#count = 0
#while count < 1:
#    ser.write("4")
#    sleep(1)
#    msg = ser.read(ser.inWaiting())
#    count += 1
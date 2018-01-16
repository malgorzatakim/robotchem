"""
Class responsible for platform movement.
Contains functions that move the platform up or down by specified number of steps (multiples of 0.1 mm)
as well as a function that moves the platform all the way down until it hits the button
"""

import serial
from time import sleep

class Platform:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyACM0', 9600) #connects to the arduino device at baud rate of 9600
        #pass

    def moveUp(self, steps):
        print "Moving up by: {} steps".format(steps)
        for _ in range(steps):
            #pass
            self.serial.write("1") # "1" is the signal for arduino to move up
            sleep(0.1) # sleep for how long it takes for the platform to move by steps
    def moveDown(self, steps):
        print "Moving down by: {} steps".format(steps)
        for _ in range(steps):
            #pass
            self.serial.write("2") # "2" is the signal for arduino to move down
            sleep(0.1)

    def moveDownAll(self): #moves the platform all way down
        #pass
        self.serial.write("4") # "4" is the signal for arduino to move all the way down
        sleep(5) # sleep for the maximum time necessary for the platform to move down

import serial

class Platform:
	def __init__(self):
		self.serial = serial.Serial('/dev/ttyACM0', 9600)
    
    def moveUp(self):
        self.serial.write(1)

    def moveDown(self):
        self.serial.write(2)

    def moveDownAll(self):
    	pass

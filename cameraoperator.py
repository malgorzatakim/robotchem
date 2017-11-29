from PyQt4 import QtGui
import picamera

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath 
        self.camera = picamera.PiCamera()
        
    def takePic(self):
    	self.camera.capture()
        return QtGui.QPixmap(self.imageBasePath + "kolpak.jpg")

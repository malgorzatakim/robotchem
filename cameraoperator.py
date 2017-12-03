from PyQt4 import QtGui
from PIL import Image
#import picamera

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath 
        #self.camera = picamera.PiCamera()
        
    def takePic(self):
        #self.camera.capture("kolpak.jpg")
        return Image.open(self.imageBasePath + "kolpak.jpg")
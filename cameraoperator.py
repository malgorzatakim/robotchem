from PyQt4 import QtGui
from PIL import Image
import time
import os
#import picamera

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath
        #self.camera = picamera.PiCamera()
        
    def takePic(self): #, path):
        #self.camera.capture("kolpak.jpg")
        #return Image.open(str(path) + "kolpak.jpg")
        return Image.open(self.imageBasePath + "kolpak.jpg")

    def newSubfolder(self): #, name):
        name = time.time()
        return os.mkdir(self.imageBasePath + str(name))
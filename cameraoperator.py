from PyQt4 import QtGui
from PIL import Image
import time
import os
from shutil import copy2
#import picamera

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath
        #self.camera = picamera.PiCamera()
        
    def takePic(self, path):
        #self.camera.capture(path + "kolpak.jpg")
        filename = "kolpak.jpg"
        copy2(self.imageBasePath + filename, path + filename)
        return Image.open(path + filename)

    def newSubfolder(self):
        name = time.time()
        directory = self.imageBasePath + str(name) + "/"
        os.mkdir(directory)
        return directory
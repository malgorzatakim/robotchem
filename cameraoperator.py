from PyQt4 import QtGui
from PIL import Image
import time
import os
from shutil import copy2
#import picamera

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath
        self.currentSubfolder = self.imageBasePath
        #self.camera = picamera.PiCamera()
        
    def takePic(self):
        #self.camera.capture(path + "kolpak.jpg")
        filename = "kolpak.jpg"
        copy2(self.imageBasePath + filename, self.currentSubfolder + filename)
        return Image.open(self.currentSubfolder + filename)

    def newSubfolder(self):
        name = time.time()
        self.currentSubfolder = self.imageBasePath + str(name) + "/"
        os.mkdir(self.currentSubfolder)
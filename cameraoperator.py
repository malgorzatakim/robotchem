from PyQt4 import QtGui
from PIL import Image
import time
import os
from shutil import copy2
import picamera
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath
        self.currentSubfolder = self.imageBasePath
        self.camera = picamera.PiCamera()
        
    def takePic(self):
        #filename = "kolpak.png"
        filename = str(int(time.time() * 100)) + ".png"
        self.camera.capture(self.currentSubfolder + filename)
        #copy2(self.imageBasePath + filename, self.currentSubfolder + filename)
        return Image.open(self.currentSubfolder + filename), filename

    def newSubfolder(self):
        name = time.time()
        self.currentSubfolder = self.imageBasePath + str(name) + "/"
        os.mkdir(self.currentSubfolder)

    def getCurrentSubfolder(self):
        return self.currentSubfolder
from PyQt4 import QtGui
from PIL import Image
import time
import os
from shutil import copy2
import picamera
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True # error prevention for display of large images

class CameraOperator:
    def __init__(self, basePath):
        self.imageBasePath = basePath
        self.currentSubfolder = self.imageBasePath
        self.camera = picamera.PiCamera()

    def takePic(self):
        src = "kolpak.png"
        filename = str(int(time.time() * 100)) + ".png" # *100 because filenames can't have "."
        self.camera.capture(self.currentSubfolder + filename) # takes a picture and puts it in a folder
        # copy2(self.imageBasePath + src, self.currentSubfolder + filename) # for testing on a non-raspberry pi computer
        return Image.open(self.currentSubfolder + filename), filename

    def newSubfolder(self): # creates a new subfolder (called with timestamp) for a new dataset (either single pic or autofocus)
        name = time.time()
        self.currentSubfolder = self.imageBasePath + str(name) + "/" # name of the subfolder
        os.mkdir(self.currentSubfolder)

    def getCurrentSubfolder(self):
        return self.currentSubfolder
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
        self.camera.resolution = (3000, 2000)
        src = "kolpak.png"
        filename = str(int(time.time() * 100)) + ".png" # *100 because filenames can't have "."
        self.camera.capture(self.currentSubfolder + filename) # takes a picture and puts it in a folder
        #copy2(self.imageBasePath + src, self.currentSubfolder + filename) # for testing on a non-raspberry pi computer
        image = Image.open(self.currentSubfolder + filename)
        #opening the picture and cropping
        print(image.size)
        image2 = image.crop((980, 760, 1810, 1590))
        image2.save(self.currentSubfolder + filename)
        return image2, filename

    def newSubfolder(self, masterFolder): # creates a new subfolder (called with timestamp) for a new dataset (either single pic or autofocus)
        name = time.time()
        self.currentSubfolder = self.imageBasePath + masterFolder + "/" + str(name) + "/" # name of the subfolder
        os.makedirs(self.currentSubfolder)

    def getCurrentSubfolder(self):
        return self.currentSubfolder
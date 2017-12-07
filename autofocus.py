from PIL import Image
import numpy as np
from cameraoperator import CameraOperator
from platform import Platform

class Autofocus:

    def __init__(self, CameraOperator, Platform, Main):
        self.cameraOperator = CameraOperator
        self.platform = Platform
        self.main = Main

    def runAutofocus(self):
        self.cameraOperator.newSubfolder()
        image = self.cameraOperator.takePic()
        self.main.displayPic(image)
        focusnumber = self.__calcFocusing__(image)

    def stopAutofocus(self):
        pass

    def __calcFocusing__(self, image):
        im = image.convert("L") #opens pic and converts to grayscale
        width, height = im.size #gets image dimensions
        pixels = np.array(list(im.getdata())) #creates a list of all the pixel intensities
        mean = np.mean(pixels) #calculates mean intensity of the picture
        if mean != 0: #so that we dont divide by 0
            focusing = 1 / (height * width * mean) * (np.dot(pixels, pixels) 
                -  2 * mean * np.sum(pixels) + mean * mean * pixels.size)
        print focusing
        return focusing



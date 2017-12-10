from PIL import Image
import numpy as np
from cameraoperator import CameraOperator
from platform import Platform
import time

class Autofocus:

    def __init__(self, CameraOperator, Platform, Main):
        self.cameraOperator = CameraOperator
        self.platform = Platform
        self.main = Main

        self.imagesInSweep = 13
        self.totalPositions = 1300

    def runAutofocus(self):
        maxPosition, maxFocusing, data = self.autofocusSweep()
        finalData = self.fineTuning(maxPosition, maxFocusing, data)

        summary = self.cameraOperator.getCurrentSubfolder()
        with open(summary, "w") as f:
            for i in range(finalData):
                f.write("{}, {}, {}\n".format(finalData[i][0], finalData[i][1], finalData[i][2]))

    def stopAutofocus(self):
        pass

    def autofocusSweep(self):
        self.platform.MoveDownAll()

        position = 0 
        data = []
        for _ in range(imagesInSweep):
            self.__captureAndFocusing__(position, data)
            position += maxSteps
            self.platform.MoveUp(maxSteps) 

        maxFocusing = -1
        maxPosition = -1
        for i in range(len(data)): #find highest focusNumber and the corresponding position
            if data[i][1] > maxFocusing:
                maxFocusing = data[i][1]
                maxPosition = data[i][0]

        self.platform.MoveDown(position - maxPosition) #move to the position of highest focusNumber

        return maxPosition, maxFocusing, data

    def fineTuning(self, maxPosition, maxFocusing, data):
        steps = self.totalPositions // self.imagesInSweep
        focusStart = maxFocusing

        while steps >= 1:
            self.platform.MoveUp(steps)
            position += steps
            focusNew = self.__captureAndFocusing__(position, data)

            if focusNew > focusStart:
                focusStart = focusNew
            else:
                self.platform.moveDown(2 * steps)
                position -= 2 * steps
                focusNew = self.__captureAndFocusing__(position, data)

                if focusNew > focusStart:
                    focusStart = focusNew
                else:
                    self.platform.moveUp(steps)
                    position += steps
            steps // 2

        return data

    def __captureAndFocusing__(self, position, data):
        image, filename = self.cameraOperator.takePic()
        self.main.displayPic(image)
        focus = self.__calcFocusing__(image)
        data.append((position, focus, filename))
        return focus


    def __calcFocusing__(self, image):
        im = image.convert("L") #opens pic and converts to grayscale
        width, height = im.size #gets image dimensions
        #pixels = list(im.getdata())
        pixels = np.array(list(im.getdata()), dtype = "int64") #creates a list of all the pixel intensities
        mean = np.mean(pixels) #calculates mean intensity of the picture
        if mean != 0: #so that we dont divide by 0
            #focusing = 1 / (height * width * mean) * sum([(x - mean) * (x - mean) for x in pixels])
            focusing = 1 / (height * width * mean) * (np.dot(pixels, pixels)
                -  2 * mean * np.sum(pixels) + mean * mean * pixels.shape[0])
        print focusing
        return focusing

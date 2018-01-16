"""
Class containing all the autofocusing functionality
The calculations are based on the mean intensity focusing value comparing the intensity of every pixel with the mean intensity of all pixels
and hence determines its sharpness
The algorithm performs a sweep across a range of positions folllowed by fine tuning of the positions around the maximum focsuing value
from the sweep
"""
from PIL import Image, ImageFile
import numpy as np
from cameraoperator import CameraOperator
from platform import Platform
import time
import matplotlib.pyplot as plt
from plot import PlotFocusing
from PyQt4.QtCore import SIGNAL

ImageFile.LOAD_TRUNCATED_IMAGES = True # error prevention for display of large images

class Autofocus:

    def __init__(self, cameraOperator, platform, thread):
        self.cameraOperator = cameraOperator
        self.platform = platform
        self.plotFocusing = PlotFocusing(cameraOperator)
        self.thread = thread

        self.totalPositions = 500 # hardcoded value
        self.maxSteps = 50 # hardcoded  value
        self.imagesInSweep = self.totalPositions // self.maxSteps - 1 # sweep does not include extreme positions

    def runAutofocus(self, masterFolder):
        self.cameraOperator.newSubfolder(masterFolder)
        maxPosition, maxFocusing, data = self._autofocusSweep()
        position, finalData = self._fineTuning(maxPosition, maxFocusing, data)

        finalFocusing = -1

        for i in range(len(finalData)): # to obtain the filename and focusing of the best picture
            if finalData[i][0] == position:
                finalFocusing = finalData[i][1]
                finalFilename = finalData[i][2]
        print position

        image = Image.open(self.cameraOperator.getCurrentSubfolder() + finalFilename) # displays the best picture at the end
        #self.main.displayPic(image) # lines from before threading was introduced
        self.thread.emit(SIGNAL('displayPic'), image) # sends info to thread to displayPic
        self.plotFocusing.plotting(finalData) # plots focusing values vs. position

        summary = self.cameraOperator.getCurrentSubfolder() + "summary.txt" # creates a summary file with all the data and best data
        with open(summary, "w") as f:
            f.write("The most focused picture is: {} at position {} with focus value of {}\n".format(finalFilename, position, finalFocusing))
            for entry in finalData:
                f.write("{}, {}, {}\n".format(entry[0], entry[1], entry[2]))

    def stopAutofocus(self):
        pass

    def _autofocusSweep(self):
        self.platform.moveDownAll() # to get zero position

        position = 0
        data = []
        for _ in range(self.imagesInSweep): # move first then capture across the whole platform range
            self.platform.moveUp(self.maxSteps)
            position += self.maxSteps
            self._captureAndFocusing(position, data)

        maxFocusing = -1
        maxPosition = -1
        for i in range(len(data)): # find highest focusNumber and the corresponding position
            if data[i][1] > maxFocusing:
                maxFocusing = data[i][1]
                maxPosition = data[i][0]

        self.platform.moveDown(position - maxPosition) # move to the position of highest focusNumber

        return maxPosition, maxFocusing, data

# _FineTuning operates on the range of 2 * imagesInSweep with the middle position with maxFocusing from sweep.
# Halves the number of steps, moves from the maxFocsuing position (either way), compares the focusing value
# and chooses the new maxFocusing. These are repeated until step is minimal.

    def _fineTuning(self, maxPosition, maxFocusing, data):
        steps = self.maxSteps // 2
        focusStart = maxFocusing
        position = maxPosition

        while steps >= 1:
            self.platform.moveUp(steps)
            position += steps
            focusNew = self._captureAndFocusing(position, data)

            if focusNew > focusStart:
                focusStart = focusNew
            else:
                self.platform.moveDown(2 * steps)
                position -= 2 * steps
                focusNew = self._captureAndFocusing(position, data)

                if focusNew > focusStart:
                    focusStart = focusNew
                else:
                    self.platform.moveUp(steps)
                    position += steps
            steps //= 2

        return position, data

    def _captureAndFocusing(self, position, data):
        image, filename = self.cameraOperator.takePic()
        self.thread.emit(SIGNAL('displayPic'), image) # send signal to threading to displayPic
        time.sleep(1)
        #focus = - (position- 63) ** 2 + 3000 # mathematical function simulating the focusing values (parabola)
        focus = self._calcFocusing(image)
        data.append((position, focus, filename))
        return focus


    def _calcFocusing(self, image): # calculates the focusing value of an image accoridng to the mean intensity formula
        im = image.convert("L") # opens pic and converts to grayscale
        width, height = im.size # gets image dimensions
        # pixels = list(im.getdata())
        pixels = np.array(list(im.getdata()), dtype = "int64") # creates a list of all the pixel intensities
        mean = np.mean(pixels) #calculates mean intensity of the picture
        if mean != 0: # so that we dont divide by 0
            #focusing = 1 / (height * width * mean) * sum([(x - mean) ** 2 for x in pixels])
            focusing = 1 / (height * width * mean) * (np.dot(pixels, pixels)
                -  2 * mean * np.sum(pixels) + mean * mean * pixels.shape[0]) # optimised (faster) calculation of the focusing value
        else:
            focusing = 0
        print focusing
        return focusing
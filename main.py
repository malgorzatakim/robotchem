"""
Contains two classes:
BackgroundThread - responsible for threading actions from other clasess
that results in real time updates of pictures in GUI
Main - the main class that gathers all the functionality of the program; contains the GUI made with QT Creator and PYQT4
as well as functionality of all the components (buttons, labels)
"""


import sys
import time
from PyQt4 import QtGui, QtCore
from PIL.ImageQt import ImageQt
from gui import Ui_MainWindow
from cameraoperator import CameraOperator
from autofocus import Autofocus
from platform import Platform
from scheduler import Scheduler
from plot import PlotFocusing
from PyQt4.QtCore import QThread, SIGNAL

class BackgroundThread(QThread): # threading for background image display from autofocus and scheduler

    def __init__(self, cameraOperator, platform, main):
        QThread.__init__(self)
        self.autofocus = Autofocus(cameraOperator, platform, self)
        self.scheduler = Scheduler(self.autofocus)
        self.main = main

    def stop(self): # ???
        self.quit()
        self.wait()

    def __del__(self): # ???
        self.quit()
        self.wait()

    def run(self):
        masterFolder = "master_" + str(time.time())
        if self.main.backgroundMode == 1: # turns on autofocus threading
            self.autofocus.runAutofocus(masterFolder)
        elif self.main.backgroundMode == 2: # turns on scheduler threading
            print "Starting scheduled runs for {} sec with min intervals of {} sec".format(*self.main.schedulerArgs)
            #print used as a debugging control
            self.scheduler.startSerial(*self.main.schedulerArgs, masterFolder = masterFolder) # turns on scheduelr threading, arguments unpacked with *
        else:
            print "Unknown background mode."

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnTakePic.clicked.connect(self.takePicClicked) # when an object btnTakePic is clicked run function self.takePicClicked
        self.ui.btnAutofocus.clicked.connect(self.autofocusClicked)
        self.ui.btnMoveUp.clicked.connect(self.moveUpClicked)
        self.ui.btnMoveDown.clicked.connect(self.moveDownClicked)
        self.ui.btnStart.clicked.connect(self.startClicked)
        self.ui.btnStop.clicked.connect(self.stopClicked)


        self.cameraOperator = CameraOperator("./images/") # basepath for the results (within robotchem folder)
        self.platform = Platform()

        self.backgroundThread = BackgroundThread(self.cameraOperator, self.platform, self)
        self.connect(self.backgroundThread, SIGNAL("displayPic"), self.displayPic)
        self.backgroundMode = 0 # initialisation of the backgroundMode variable

    def takePicClicked(self): # take picture, put it in a folder and display it
        if self._processRunning(): # checks whether a background process is running
            return
        self.cameraOperator.newSubfolder()
        image, _ = self.cameraOperator.takePic() # takes a picture and puts it in the created subfolder
        self.displayPic(image)

    def displayPic(self, image): #displys a picture
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image)) # transform an image file into pixmap
        # display image in labPic label that fits into its size and maintains the aspect ratio
        self.ui.labPic.setPixmap(pixmap.scaled(self.ui.labPic.size(), QtCore.Qt.KeepAspectRatio))

    def autofocusClicked(self): # run the autofocus program
        if self._processRunning():
            return
        self.backgroundMode = 1
        self.backgroundThread.start() #start uses run (from backgroundThread class)

    def moveUpClicked(self):
        if self._processRunning():
            return
        self.platform.moveUp(5) # move the platform up by a specified number of steps (multiplies of 0.1 mm)

    def moveDownClicked(self):
        if self._processRunning():
            return
        self.platform.moveDown(5) # move the platform down by a specified number of steps (multiplies of 0.1 mm)

    def startClicked(self): # run the scheduler program
        if self._processRunning():
            return
        self.backgroundMode = 2
        # read the values of time and interval from GUI spinners and pass them to the scheduler function
        self.schedulerArgs = (self.ui.spinTime.value(), self.ui.spinInterval.value())
        self.backgroundThread.start()

    def stopClicked(self): # placeholder
        if self._processRunning():
            return

    def _processRunning(self): # checks whether another process is running - if so, rejects an action (prevents from clicking buttons)
        if self.backgroundThread.isRunning():
            print "Background process running. Rejecting requested action."
            return True
        else:
            return False

if __name__ == '__main__': # ???
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

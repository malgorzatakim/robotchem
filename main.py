import sys
from PyQt4 import QtGui, QtCore
from PIL.ImageQt import ImageQt
from gui import Ui_MainWindow
from cameraoperator import CameraOperator
from autofocus import Autofocus
from platform import Platform
from scheduler import Scheduler
from plot import PlotFocusing
from PyQt4.QtCore import QThread, SIGNAL

class BackgroundThread(QThread):

    def __init__(self, cameraOperator, platform, plotFocusing, main):
        QThread.__init__(self)
        self.autofocus = Autofocus(cameraOperator, platform, plotFocusing, self)
        self.scheduler = Scheduler(self.autofocus)
        self.main = main

    def stop(self):
        self.quit()
        self.wait()

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        if self.main.backgroundMode == 1:
            self.autofocus.runAutofocus()
        elif self.main.backgroundMode == 2:
            print "Starting scheduled runs for {} sec with min intervals of {} sec".format(*self.main.schedulerArgs)
            self.scheduler.startSerial(*self.main.schedulerArgs) # arguments unpacked with *
        else:
            print "Unknown background mode."

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnTakePic.clicked.connect(self.takePicClicked)
        self.ui.btnAutofocus.clicked.connect(self.autofocusClicked)
        self.ui.btnMoveUp.clicked.connect(self.moveUpClicked)
        self.ui.btnMoveDown.clicked.connect(self.moveDownClicked)
        self.ui.btnStart.clicked.connect(self.startClicked)
        self.ui.btnStop.clicked.connect(self.stopClicked)


        self.cameraOperator = CameraOperator("./images/")
        self.platform = Platform()
        self.plotFocusing = PlotFocusing(self.cameraOperator)

        self.backgroundThread = BackgroundThread(self.cameraOperator, self.platform, self.plotFocusing, self)
        self.connect(self.backgroundThread, SIGNAL("displayPic"), self.displayPic)
        self.backgroundMode = 0

    def takePicClicked(self):
        if self.__processRunning__():
            return
        self.cameraOperator.newSubfolder()
        image, _ = self.cameraOperator.takePic()
        self.displayPic(image)

    def displayPic(self, image):
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        #self.ui.labPic.setScaledContents(True)
        #self.ui.labPic.setPixmap(pixmap)
        self.ui.labPic.setPixmap(pixmap.scaled(self.ui.labPic.size(), QtCore.Qt.KeepAspectRatio))

    def autofocusClicked(self):
        if self.__processRunning__():
            return
        self.backgroundMode = 1
        self.backgroundThread.start() #start uses run (from backgroundThread class)

    def moveUpClicked(self):
        if self.__processRunning__():
            return
        self.platform.moveUp(50)

    def moveDownClicked(self):
        if self.__processRunning__():
            return
        self.platform.moveDown(50)

    def startClicked(self):
        if self.__processRunning__():
            return
        self.backgroundMode = 2
        self.schedulerArgs = (self.ui.spinTime.value(), self.ui.spinInterval.value())
        self.backgroundThread.start()

    def stopClicked(self):
        if self.__processRunning__():
            return

    def __processRunning__(self):
        if self.backgroundThread.isRunning():
            print "Background process running. Rejecting requested action."
            return True
        else:
            return False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

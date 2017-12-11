import sys
from PyQt4 import QtGui, QtCore
from PIL.ImageQt import ImageQt
from gui import Ui_MainWindow
from cameraoperator import CameraOperator
from autofocus import Autofocus
from platform import Platform
from scheduler import Scheduler
from plot import PlotFocusing

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
        self.plotFocusing = PlotFocusing(self.cameraOperator, self)
        self.autofocus = Autofocus(self.cameraOperator, self.platform, self.plotFocusing, self)
        self.scheduler = Scheduler(self.autofocus)

    def takePicClicked(self):    
        self.cameraOperator.newSubfolder()
        image, _ = self.cameraOperator.takePic()
        self.displayPic(image)

    def displayPic(self, image):
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        #self.ui.labPic.setScaledContents(True)
        #self.ui.labPic.setPixmap(pixmap)
        self.ui.labPic.setPixmap(pixmap.scaled(self.ui.labPic.size(), QtCore.Qt.KeepAspectRatio))

    def autofocusClicked(self):
        self.autofocus.runAutofocus()
    
    def moveUpClicked(self):
        self.platform.MoveUp(1)
    
    def moveDownClicked(self):
        self.platform.MoveDown(1)  
    
    def startClicked(self):
        self.scheduler.startSerial(self.ui.spinTime.value(), self.ui.spinInterval.value())
    
    def stopClicked(self):
        self.ui.labPlot.setText("Stop")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
        

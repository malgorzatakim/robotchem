import sys
from PyQt4 import QtGui
from gui import Ui_MainWindow
from cameraoperator import CameraOperator
from autofocus import Autofocus
from platform import Platform
from scheduler import Scheduler

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
 

        self.cameraOperator = CameraOperator("/Users/maglorzatanguyen/Desktop/")
        self.autofocus = Autofocus()
        self.platform = Platform()
        self.scheduler = Scheduler(self.autofocus)

    def takePicClicked(self):    
        self.ui.txtResult.setText("TakePic")
        pixmap = self.cameraOperator.takePic()
        self.ui.labPic.setScaledContents(True)
        self.ui.labPic.setPixmap(pixmap)

    def autofocusClicked(self):
        self.ui.txtResult.setText("Autofocus")
    
    def moveUpClicked(self):
        self.ui.txtResult.setText("MoveUp")    
    
    def moveDownClicked(self):
        self.ui.txtResult.setText("MoveDown")    
    
    def startClicked(self):
        self.ui.txtResult.setText("Start")
        self.scheduler.startSerial(self.ui.spinTime.value(), self.ui.spinInterval.value())
    
    def stopClicked(self):
        self.ui.txtResult.setText("Stop")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
        

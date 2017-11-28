import sys
from PyQt4 import QtGui
from gui import Ui_MainWindow

class Main(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.btnTakePic.clicked.connect(self.TakePic_clicked)
		self.ui.btnAutofocus.clicked.connect(self.Autofocus_clicked)
		self.ui.btnMoveUp.clicked.connect(self.MoveUp_clicked)
		self.ui.btnMoveDown.clicked.connect(self.MoveDown_clicked)
		self.ui.btnStart.clicked.connect(self.Start_clicked)
		self.ui.btnStop.clicked.connect(self.Stop_clicked)
	def TakePic_clicked(self):	
		self.ui.txtResult.setText("MoveUp")	
		pixmap = QtGui.QPixmap("/Users/maglorzatanguyen/Desktop/helga.png")
		self.ui.labPic.setScaledContents(True)
		self.ui.labPic.setPixmap(pixmap)
	def Autofocus_clicked(self):
		self.ui.txtResult.setText("Autofocus")
	def MoveUp_clicked(self):
		self.ui.txtResult.setText("MoveUp")	
	def MoveDown_clicked(self):
		self.ui.txtResult.setText("MoveDown")	
	def Start_clicked(self):
		self.ui.txtResult.setText("Start")
	def Stop_clicked(self):
		self.ui.txtResult.setText("Stop")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = Main()
	window.show()
	sys.exit(app.exec_())
		

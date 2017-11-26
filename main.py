import sys
from PyQt4 import QtGui
from gui import Ui_MainWindow

class Main(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.btn.clicked.connect(self.btn_clicked)
	
	def btn_clicked(self):
		self.ui.txtResult.setText("hello")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = Main()
	window.show()
	sys.exit(app.exec_())
		

from PyQt4 import QtGui

class CameraOperator:
    def __init__(self, basePath):
    	self.imageBasePath = basePath 
    	
    def takePic(self):
	    return QtGui.QPixmap(self.imageBasePath + "kolpak.jpg")
import matplotlib.pyplot as plt
from PIL import Image
from cameraoperator import CameraOperator


class PlotFocusing:
    def __init__(self, CameraOperator, Main):
        self.cameraOperator = CameraOperator
        self.main = Main

    def plotting(self, finalData):

        position = []
        focusing = []
        for entry in finalData:
            position.append(entry[0] // 10)
            focusing.append(entry[1])
        plt.scatter(position, focusing, linewidth = 2.0)
        plt.xlabel("position (mm)")
        plt.ylabel("focusing value (a.u.)")
        plt.savefig(self.cameraOperator.getCurrentSubfolder() + "summary_plot.png")

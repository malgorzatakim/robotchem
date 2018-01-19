"""Class responsible for plotting of the final data
"""
import matplotlib.pyplot as plt
from cameraoperator import CameraOperator

class PlotFocusing:
    def __init__(self, cameraOperator):
        self.cameraOperator = cameraOperator

    def plotting(self, finalData):
        position = []
        focusing = []
        #xmarks= [i for i in range(0,11)]
        for entry in finalData:
            position.append(entry[0] / 20.0)
            focusing.append(entry[1])
            #focusing.append(entry[1]/ 100.0)
        #plt.figure()
        plt.scatter(position, focusing, linewidth = 2.0)
        #plt.xticks(xmarks)
        #plt.annotate('(Ps, Fs)', xy = (6.0, 29.96), xytext=(5.5, 31))
        plt.xlabel("position (mm)")
        plt.ylabel("focusing value (a.u.)")
        plt.savefig(self.cameraOperator.getCurrentSubfolder() + "summary_plot.png")

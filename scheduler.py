"""
A class containing the method that autofocuses the picture over a given period of time with a given interval.
For remote observation of changes over time.
"""


from time import sleep, time

class Scheduler:

    def __init__(self, autofocus):
        self.autofocus = autofocus

    def startSerial(self, totalTime, interval, masterFolder):
        # here: interval and totalTime is in seconds
        if interval > totalTime:
            print("error, interval cannot be larger than time")
        else:
            end = time() + totalTime # calculates the end time for the measurement
            while time() < end:
                before = time() # time before exectuing autofocus
                self.autofocus.runAutofocus(masterFolder)
                duration = time() - before # how long autofocus took
                if interval > duration: # before exection of the next autofocus in series wait for the remaining time of interval
                    sleep(interval - duration)

    def stopSerial(self): # placeholder
        pass
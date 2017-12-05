from time import sleep, time

class Scheduler:

    def __init__(self, autofocus):
        self.autofocus = autofocus

    def startSerial(self, totalTime, interval):
        # here: interval and totalTime is in seconds
        if interval > totalTime:
            print("error, interval cannot be larger than time")
        else:
            end = time() + totalTime 
            while time() < end:
                before = time()
                print(self.autofocus)
                duration = time() - before
                if interval > duration:
                    sleep(interval - duration)
                
    def stopSerial(self):
        pass
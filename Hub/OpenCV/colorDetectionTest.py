from __future__ import print_function
from colorDetectionWebCamera import *
import threading
import time
import __builtin__

colorRanges = {
    'Red': [([0, 150, 50], [10, 255, 255]), ([170, 150, 50], [180, 255, 255])],
    'Green': [([30, 40, 5], [90, 255, 255])],
    'Blue': [([100, 40, 5], [130, 255, 255])],
    'Yellow': [([20, 40, 40], [35, 255, 255])]
}

def Main():
    testDetector = ColorDetectionWebCamera(colorRanges, _show=True, _threshold=500)
    #detectThread = threading.Thread(target=testDetector.startDetection)
    #detectThread.start()
    testDetector.startDetection();
    while True:
        #for color in colorRanges:
        #   if testDetector.isDetected(color):
        #        print(color + " Detected!")
        time.sleep(0.5)

if __name__ == '__main__':
    Main()

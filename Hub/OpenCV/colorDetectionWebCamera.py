# import the necessary packages
import numpy as np
import time
import cv2
import threading

class ColorDetectionWebCamera():


    def __init__(self, _colorRanges, _threshold=1000, _show=False):
        self.colorRanges = _colorRanges
        self.threshold = _threshold
        self.detected = {}
        self.show = _show
        self.camera = cv2.VideoCapture(0)
        self.lock = threading.Lock()
        self.detecting = False
        self.outputImages = {}
        for key in self.colorRanges:
            self.detected[key] = False
            self.outputImages[key] = None


    def getColorRanges(self):
        self.lock.acquire()
        toReturn = self.colorRanges
        self.lock.release()
        return toReturn


    def getThreshold(self):
        self.lock.acquire()
        toReturn = self.threshold
        self.lock.release()
        return toReturn


    def setDetected(self, color, booleanVal):
        self.lock.acquire()
        self.detected[color] = booleanVal
        self.lock.release()


    def isDetected(self, color):
        self.lock.acquire()
        toReturn = self.detected[color]
        self.lock.release()
        return toReturn


    def setDetecting(self, booleanVal):
        self.lock.acquire()
        self.detecting = booleanVal
        self.lock.release()


    def stopDetection(self):
        setDetecting(False)


    def isDetecting(self):
        self.lock.acquire()
        toReturn = self.detecting
        self.lock.release()
        return toReturn


    def addToOutputImages(self, color, image):
        self.lock.acquire()
        self.outputImages[color] = image
        self.lock.release()


    def showImages(self):
        self.lock.acquire()
        for image in self.outputImages:
            cv2.imshow(image, self.outputImages[image])
        self.lock.release()


    def detectSingleColor(self, color, hsvImage):
        colorRange = self.getColorRanges()
        thresh = self.getThreshold()
        masks = []
        # loop over the boundaries
        for (lower, upper) in self.colorRanges[color]:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")

            # find the colors within the specified boundaries and apply the mask
            masks.append(cv2.inRange(hsvImage, lower, upper))

        overallMask = masks[0]
        for mask in masks:
            overallMask = cv2.bitwise_or(mask, overallMask)

        outputImage = cv2.bitwise_and(hsvImage, hsvImage, mask=overallMask)
        self.addToOutputImages(color, outputImage)
        nonzero = cv2.countNonZero(cv2.cvtColor(outputImage, cv2.COLOR_BGR2GRAY))
        if nonzero > thresh:
            self.setDetected(color, True)
        else:
            self.setDetected(color, False)



    def startDetection(self):
        self.setDetecting(True)
        while (True):
            start_time = time.time()
            ret, image = self.camera.read()
            hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            threads = []

            # loop over all colors and start a detection thread for them
            for color in self.getColorRanges():
                colorThread = threading.Thread(target = self.detectSingleColor, args=(color, hsvImage))
                threads.append(colorThread)
                colorThread.start()

            for thread in threads:
                thread.join()

            self.addToOutputImages("original", image);

            print("----- " + str(time.time() - start_time) + " seconds -----")

            if self.show:
                self.showImages()

            cv2.waitKey(10)
            if self.isDetecting() == False:
                self.camera.release()
                cv2.destroyAllWindows()
                return

# import the necessary packages
import numpy as np
import time
import cv2
import threading

class ColorDetectionWebCamera():


    def __init__(self, _colorRanges, _threshold=1000, _show=False, _ignore=True):
        self.colorRanges = _colorRanges
        self.threshold = _threshold
        self.detected = {}
        self.show = _show
        self.ignore = _ignore
        self.whiteMask = None
        self.camera = cv2.VideoCapture(0)
        self.lock = threading.Lock()
        self.detecting = False
        self.running = True
        self.outputImages = {}
        self.detectedSample = {}
        self.myColors = {"Red" : (0, 0, 255, 255),
                         "Blue" : (255, 0, 0, 255),
                         "Green" : (0, 255, 0, 255),
                         "Yellow" : (0, 255, 255 ,255)}
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


    def initializeBoundary(self):
        if self.ignore == False:
            return
        else:
            for i in range(5):
                ret, image = self.camera.read()
                lower = [0, 0, 100]
                upper = [172, 111, 255]
                hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                if (self.whiteMask == None):
                    self.whiteMask = cv2.inRange(hsvImage, np.array(lower, dtype = np.uint8), np.array(upper, dtype = np.uint8))
                else:
                    self.whiteMask = cv2.bitwise_or(self.whiteMask, cv2.inRange(hsvImage, np.array(lower, dtype = np.uint8), np.array(upper, dtype = np.uint8)))
            
    def writeText(self, image, text, pos, color):
        cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)             


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
        if self.ignore == True:
            outputImage = cv2.bitwise_and(outputImage, outputImage, mask=self.whiteMask)
       
        nonzero = cv2.countNonZero(cv2.cvtColor(outputImage, cv2.COLOR_BGR2GRAY))
        if nonzero > thresh:
            if (self.detectedSample[color] == None):
                self.detectedSample[color] = 1
            else:
                self.detectedSample[color] = self.detectedSample[color] + 1
        else:
            self.detectedSample[color] = 0

        if (self.detectedSample[color] > 3):
            self.writeText(outputImage, "DETECTED!", (100, 100), self.myColors["Green"]) 
            self.setDetected(color, True)
        else:
            self.writeText(outputImage, "NOT DETECTED!", (100, 100), self.myColors["Red"]) 
            self.setDetected(color, False)

        self.addToOutputImages(color, outputImage)


    def startDetection(self):
        self.setDetecting(True)
        self.initializeBoundary()
        while (self.running):
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
            self.addToOutputImages("play area", self.whiteMask)

            if self.show:
                self.showImages()

            cv2.waitKey(10)
            if self.isDetecting() == False:
                self.camera.release()
                cv2.destroyAllWindows()
                return

import cv2
import time
import numpy as np

camera = cv2.VideoCapture(0)

while True:    
    ret, image = camera.read()
    lower = [0, 0, 100]
    upper = [172, 111, 255]
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    whiteMask = cv2.inRange(hsvImage, np.array(lower, dtype = np.uint8), np.array(upper, dtype = np.uint8))
    #outputImage = cv2.bitwise_and(image, image, mask=whiteMask)
    cv2.imshow('Mask', whiteMask)
    cv2.imshow('Original Image', image)
    #cv2.imshow('Output Image', outputImage)
    cv2.waitKey(100)


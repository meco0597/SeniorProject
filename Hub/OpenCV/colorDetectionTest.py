from colorDetectionPiCamera import *

colorRanges = { 'Red': [([0, 70, 50], [10, 255, 255]), ([170, 70, 50], [180, 255, 255])],
                'Green': [([40, 40, 40], [70, 255, 255])],
                'Blue': [([111, 140, 40], [126, 255, 255])],
                'Yellow': [([20, 40, 40], [35, 255, 255])]
                }


def Main():
    testDetector = ColorDetection(colorRanges, _show=True)
    testDetector.startDetection()

if __name__ == '__main__':
    Main()
    

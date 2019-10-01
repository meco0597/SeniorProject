# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution(640, 480)
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# define the list of color ranges
colorRanges = [
    ([0, 50, 50], [20, 255, 255]),# red
    ([160, 50, 50], [180, 255, 255]),
    ([36, 50, 50], [70, 255, 255])
]

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start_time = time.time()
    image = frame.array
    masks = []

    # loop over the boundaries
    for (lower, upper) in colorRanges:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        masks.append(cv2.inRange(image, lower, upper))
        
    #overallMask = masks[0]
    #for mask in masks:
    #    overallMask = cv2.bitwise_or(mask, overallMask)

    redMask = cv2.bitwise_or(masks[0], masks[1])
    
    #outputRed = cv2.bitwise_and(image, image, mask=redMask)
    outputGreen = cv2.bitwise_and(image, image, mask=masks[2])
    print("-----" + str(time.time() - start_time) + " seconds ------")
    # show the images
    cv2.imshow("images", np.hstack([originalImage, outputGreen]))
    cv2.waitKey(1000)
    rawCapture.truncate(0)

camera.release()
cv2.destroyAllWindows()

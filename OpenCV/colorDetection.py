# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# define the list of color ranges
colorRanges = [
    ([17, 15, 100], [50, 56, 200]), # red
    ([86, 31, 4], [220, 88, 50]), # blue
    ([25, 146, 190], [62, 174, 250]), # yellow
    ([103, 86, 65], [145, 133, 128]) # gray
]

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

    # loop over the boundaries
    for (lower, upper) in colorRanges:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)

        # show the images
        cv2.imshow("images", np.hstack([image, output]))
        cv2.waitKey(0)
    
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
# -*- coding: utf-8 -*-
# import the necessary package
import imutils
import cv2
import numpy as np

avg=None
min_area=500
camera = cv2.VideoCapture(0)
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Despejado"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if avg is None:
		print "[INFO] starting background model..."
		avg = gray.copy().astype("float")
		continue

	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))


    #http://www.learnopencv.com/opencv-threshold-python-cpp/
    #El pixel value sería la intensidad del pixel
	thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < min_area:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Intruso Detectado"



	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)

        value = (5, 5)
        thresh = cv2.GaussianBlur(thresh, value, 0)
        image, contours, hierarchy = cv2.findContours(thresh.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if(contours):
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frameDelta,(x,y),(x+w,y+h),(0,0,255),0)
            hull = cv2.convexHull(cnt)
            drawing = np.zeros(frameDelta.shape,np.uint8)
            cv2.drawContours(drawing,[cnt],0,(255,255,0),0)
            cv2.drawContours(drawing,[hull],0,(0,255,255),0)
            cv2.imshow("drawing", drawing)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


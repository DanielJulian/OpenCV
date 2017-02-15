# -*- coding: utf-8 -*-
#Identify pupils. Based on beta 1
#https://gist.github.com/edfungus/67c14af0d5afaae5b18c


import numpy as np
import cv2
import math
import datetime
from pymouse import PyMouse

m = PyMouse()

cap = cv2.VideoCapture(0) 	#640,480
w = 640
h = 480



while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:


		#detect eyes
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		eyes = cv2.CascadeClassifier('Project2/haarcascade_eye.xml')
		detected = eyes.detectMultiScale(gray, 1.3, 5)


		pupilFrame = gray
		pupilO = gray
		windowClose = np.ones((5,5),np.uint8)
		windowOpen = np.ones((2,2),np.uint8)
		windowErode = np.ones((2,2),np.uint8)

		#draw square
		for (x,y,w,h) in detected:
			cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)
			cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
			cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)

			pupilFrame = cv2.equalizeHist(gray[y+(h*.25):(y+h), x:(x+w)])
			pupilO = pupilFrame
			ret, pupilFrame = cv2.threshold(pupilFrame,55,255,cv2.THRESH_BINARY)		#50 ..nothin 70 is better
			pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
			pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
			pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)

			#so above we do image processing to get the pupil..
			#now we find the biggest blob and get the centriod

			threshold = cv2.inRange(pupilFrame,250,255)		#get the blobs
			_, contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

			#if there are 3 or more blobs, delete the biggest and delete the left most for the right eye
			#if there are 2 blob, take the second largest
			#if there are 1 or less blobs, do nothing

			if len(contours) >= 2:
				#find biggest blob
				maxArea = 0
				MAindex = 0			#to get the unwanted frame
				distanceX = []		#delete the left most (for right eye)
				currentIndex = 0
				for cnt in contours:
					area = cv2.contourArea(cnt)
					center = cv2.moments(cnt)
					# el np.float64 se lo pongo para evitar un error de division por 0. http://stackoverflow.com/questions/10011707/how-to-get-nan-when-i-divide-by-zero
					cx,cy = np.float64(center['m10'])/center['m00'], np.float64(center['m01'])/center['m00']
					if(math.isnan(cx) or math.isnan(cy)):
						cx=int(0)
						cy=int(0)
					else:
						cx=int(cx)
						cy=int(cy)
					distanceX.append(cx)
					if area > maxArea:
						maxArea = area
						MAindex = currentIndex
					currentIndex = currentIndex + 1

				del contours[MAindex]		#remove the picture frame contour
				del distanceX[MAindex]

			eye = 'right'

			if len(contours) >= 2:		#delete the left most blob for right eye
				if eye == 'right':
					edgeOfEye = distanceX.index(min(distanceX))
				else:
					edgeOfEye = distanceX.index(max(distanceX))
				del contours[edgeOfEye]
				del distanceX[edgeOfEye]

			if len(contours) >= 1:		#get largest blob
				maxArea = 0
				for cnt in contours:
					area = cv2.contourArea(cnt)
					if area > maxArea:
						maxArea = area
						largeBlob = cnt

			if len(largeBlob) > 0:
				center = cv2.moments(largeBlob)
				cx,cy = int(np.float64(center['m10'])/center['m00']), int(np.float64(center['m01'])/center['m00'])
				cv2.circle(pupilO,(cx,cy),5,255,-1)


		#show picture
		cv2.putText(frame, (datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
		cv2.imshow("frame1",frame)
		cv2.imshow('frame3',pupilO)
		cv2.imshow('frame2',pupilFrame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	#else:
		#break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()

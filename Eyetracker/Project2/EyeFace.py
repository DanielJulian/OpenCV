# -*- coding: utf-8 -*-
#https://gist.github.com/edfungus/67c14af0d5afaae5b18c


import cv2
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
		eyes_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		detectedEyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)


		#draw square
		for (x,y,w,h) in detectedEyes:
			m.move(x,y)
			cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)
			cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
			cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)

		#show picture
		cv2.putText(frame, (datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
		cv2.imshow("Video",frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()

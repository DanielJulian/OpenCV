# -*- coding: utf-8 -*-
#https://gist.github.com/edfungus/67c14af0d5afaae5b18c


import cv2
from pymouse import PyMouse
from collections import deque

promediadorX = [0,0,0,0,0,0,0,0,0,0]
deqX = deque(promediadorX)
promediadorY = [0,0,0,0,0,0,0,0,0,0]
deqY = deque(promediadorY)
constX=0
direction=""
m = PyMouse()
mediaX=0
mediaY=0

cap = cv2.VideoCapture(0) 	#640,480
w = 640
h = 480


def moving_average(vec, n=15):
    s = sum(vec)
    return (s / n)


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

		#detect eyes
		eyes_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		detectedEyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)


		#draw square
		for (x,y,w,h) in detectedEyes:
			#m.move(x,y)
			cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)
			cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
			cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
			deqX.pop()
			deqY.pop()
			deqX.appendleft(x)
			deqY.appendleft(y)
			mediaX=moving_average(deqX)
			mediaY=moving_average(deqY)

		if(constX>mediaX):
			direction="Izquierda"
		if(constX<mediaX):
			direction="Derecha"

		cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
		cv2.putText(frame, "x: {}, y: {}".format(mediaX, mediaY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
		print ( "x: {}, y: {}, constX: {}".format(mediaX, mediaY,constX))
		#show picture
		cv2.imshow("Video",frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if cv2.waitKey(1) & 0xFF == ord('c'):
			constX=moving_average(deqX)

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()






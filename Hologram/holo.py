import cv2
import numpy as np
from pygame import mixer


mixer.init()
mixer.music.load('rwby.mp3')
mixer.set_num_channels(1)


def start():
    best_cnt=1
    webcam = cv2.VideoCapture(0)
    video = cv2.VideoCapture("rwby.mp4")
    mixer.music.play()
    while(True):
        blank_image = np.zeros((768,1024,3), np.uint8)
        flag, frame = webcam.read()
        flag2, framevid = video.read()
        framevid = cv2.resize(framevid, (250,150))
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1024,768))
        orig_frame = frame.copy();
        frame = cv2.blur(frame,(3,3))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        threshYellow = cv2.inRange(hsv,np.array((26, 80, 84)), np.array((40, 255, 255)))
        threshRed = cv2.inRange(hsv,np.array((0, 158, 182)), np.array((6, 223, 255)))
        _,contoursY,_ = cv2.findContours(threshYellow,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        _,contoursR,_ = cv2.findContours(threshRed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contoursY:
            area = cv2.contourArea(cnt)
            if area > 50:
                best_cnt = cnt

        M = cv2.moments(best_cnt)
        ycx,ycy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        print "x:",ycx,"y:",ycy

        if(ycy+150<768 and ycx+250<1024):
            blank_image[ycy:ycy+150, ycx:ycx+250] = framevid

        img_cpy = orig_frame.copy()

        opacity = 1
        #http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#addweighted
        #el resultado del addweighted se guarda en el ultimo parametro, en este caso, orig_frame
        cv2.addWeighted(img_cpy, opacity, orig_frame, 1 - opacity, 0, orig_frame)

        final = cv2.add(orig_frame,blank_image)
        cv2.imshow('thresh',threshYellow)
        cv2.imshow('final',final)


        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

start()

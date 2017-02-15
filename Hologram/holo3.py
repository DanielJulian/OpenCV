#Holo2: La disposicion de las manos tiene que ser diagonal.
import cv2
import numpy as np
from pygame import mixer


mixer.init()
mixer.music.load('rwby.mp3')
mixer.set_num_channels(1)


def start():
    best_cnt=1
    best_cnt2=1
    webcam = cv2.VideoCapture(0)
    video = cv2.VideoCapture("rwby.mp4")
    #mixer.music.play()
    flag2, framevid = video.read()
    size= framevid.shape
    pts_src = np.array(
                        [
                        [0,0], # punto del corner superior izquierdo ( X , Y )
                        [size[1] - 1, 0],  # punto del corner superior derecho( X , Y )
                        [size[1] - 1, size[0] -1], # punto del corner inferior derecho ( X , Y )
                        [0, size[0] - 1 ] # punto del corner inferior izquierdo ( X , Y )
                        ],dtype=float
                        );

    while(True):
        blank_image = np.zeros((768,1024,3), np.uint8)
        flag, frame = webcam.read()
        flag2, framevid = video.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1024,768))

        orig_frame= frame.copy()

        #Puntos de la imagen de de destino(camara web)



        frame = cv2.blur(frame,(3,3))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        threshYellow = cv2.inRange(hsv,np.array((26, 80, 84)), np.array((40, 255, 255)))
        threshRed = cv2.inRange(hsv,np.array((164, 118, 108)), np.array((215, 255, 255)))
        _,contoursY,_ = cv2.findContours(threshYellow,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        _,contoursR,_ = cv2.findContours(threshRed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contoursY:
            area = cv2.contourArea(cnt)
            if area > 50:
                best_cnt = cnt

        M = cv2.moments(best_cnt)
        ycx,ycy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        for cnt in contoursR:
            area = cv2.contourArea(cnt)
            if area > 50:
                best_cnt2 = cnt

        M = cv2.moments(best_cnt2)
        rcx,rcy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])



        #Puntos a donde warpear la imagen
        pts_dst = np.array(
                          [
                            [ycx, ycy-abs(rcx-ycx)/2], # punto del corner superior izquierdo ( X , Y )
                            [rcx - 1, rcy-abs(rcx-ycx)/2],  # punto del corner superior derecho( X , Y )
                            [rcx - 1, rcy], # punto del corner inferior derecho ( X , Y: Esta y es inclinacion horizontal )
                            [ycx, ycy ] # punto del corner inferior izquierdo ( X , Y )
                            ],dtype=float
                           );


        h, status = cv2.findHomography(pts_src, pts_dst);

        im_temp = cv2.warpPerspective(framevid, h, (1024,768))

        #framevid = cv2.resize(framevid, (rcx-ycx,rcy-ycy))
        #blank_image[ycy:rcy, ycx:rcx] = framevid
        final = cv2.add(orig_frame,im_temp)

        cv2.imshow('frame',final)
        #cv2.imshow("imtemp", im_temp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

start()

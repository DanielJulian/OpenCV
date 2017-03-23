#Holo4 _ Includes Paint.
import cv2
import numpy as np
from pygame import mixer

#Inicialize audio object
mixer.init()
mixer.music.load('rwby.mp3')
mixer.set_num_channels(1)

#Define size of video frames
width=1024
height=768


#Function that determines if "fingertip" is inside the color rectangle
def in_rectangle(x1,y1,x4,y4,cx,cy):
    if (cx>x1 and cx<x4) and (cy>y1 and cy<y4):
        return True
    return False


def start():
    #Variables for Video Stuff
    best_cnt=1
    best_cnt2=1

    #Variables for Paint Stuff
    best_cnt3=1
    blank_image = np.zeros((height,width,4), np.uint8)
    prev_x = 0
    prev_y = 0
    draw_color = (0,0,255) #Starting Color for painting

    #Prepare Stuff before Looping
    webcam = cv2.VideoCapture(0)
    video = cv2.VideoCapture("Gandalf.avi")
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

    #mixer.music.play()
    while(True):
        flag, frame = webcam.read()
        flag2, framevid = video.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (width,height))

        orig_frame= frame.copy()

        frame = cv2.blur(frame,(3,3))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        threshYellow = cv2.inRange(hsv,np.array((26, 80, 84)), np.array((40, 255, 255)))
        #threshRed = cv2.inRange(hsv,np.array((164, 118, 108)), np.array((215, 255, 255)))
        #En realidad es NARANJA
        threshRed = cv2.inRange(hsv,np.array((0, 137, 154)), np.array((17, 249, 255)))
        #threshGreen = cv2.inRange(hsv,np.array((40, 126, 188)), np.array((95, 222, 255)))
        threshGreen = cv2.inRange(hsv,np.array((82, 222, 86)), np.array((90, 255, 255)))
        _,contoursY,_ = cv2.findContours(threshYellow,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        _,contoursR,_ = cv2.findContours(threshRed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        _,contoursG,_ = cv2.findContours(threshGreen,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

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

        print abs(rcx-ycx)/2

        h, status = cv2.findHomography(pts_src, pts_dst);

        im_temp = cv2.warpPerspective(framevid, h, (width,height))
        final = cv2.add(orig_frame,im_temp)

        #7cv2.imshow('frame',final)

        #Paint part

        for cnt in contoursG:
            area = cv2.contourArea(cnt)
            if area > 50:
                best_cnt3 = cnt

        M = cv2.moments(best_cnt3)
        gcx,gcy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        if in_rectangle(551,00,600,50,gcx,gcy):
            draw_color = (255,0,0)
            print "inside3"
        if in_rectangle(501,000,550,50,gcx,gcy):
            draw_color = (0,255,0)
            print "inside2"
        if in_rectangle(450,000,500,50,gcx,gcy):
            draw_color = (0,0,255)
            print "inside1"

        if(abs(gcx-prev_x)>100 or abs(gcy-prev_y)>100):
            cv2.circle(blank_image,(gcx,gcy),5,draw_color,-1)
        else:
            cv2.line(blank_image,(gcx,gcy),(prev_x,prev_y),draw_color,3)


        img_cpy = final.copy()
        cv2.rectangle(img_cpy,(450,000),(500,50),(255,0,0),-1) #B
        cv2.rectangle(img_cpy,(500,000),(550,50),(0,255,0),-1) #g
        cv2.rectangle(img_cpy,(550,000),(600,50),(0,0,255),-1) #r

        opacity = 1
        #http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#addweighted
        #el resultado del addweighted se guarda en el ultimo parametro, en este caso, orig_frame
        cv2.addWeighted(img_cpy, opacity, final, 1 - opacity, 0, final)

        final = cv2.cvtColor(final, cv2.COLOR_BGR2RGBA)
        final = cv2.add(final,blank_image)
        final = cv2.cvtColor(final, cv2.COLOR_RGBA2BGR)
        cv2.imshow('Finalizado',final)

        prev_x = gcx
        prev_y = gcy


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

start()

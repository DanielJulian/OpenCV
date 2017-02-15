import cv2
import numpy as np
from PIL import Image, ImageTk

best_cnt = 1
blank_image = np.zeros((400,600,4), np.uint8)
cx=0
cy=0
prev_x = cx
prev_y = cy
draw_color = (255,0,0)
color_radius = 40

def set_image(lbl,img):
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    lbl.imgtk = imgtk
    lbl.configure(image=imgtk)

def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

def in_rectangle(x1,y1,x4,y4,cx,cy):
    if (cx>x1 and cx<x4) and (cy>y1 and cy<y4):
        return True
    return False

def start():
    cap = cv2.VideoCapture(0)
    global best_cnt,blank_image,prev_x,prev_y,cy,cx,draw_color
    while(True):
        flag, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (600,400))    
        orig_frame = frame.copy();
        frame = cv2.blur(frame,(3,3))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv,np.array((0, 108, 197)), np.array((73, 1945, 255)))
        thresh2 = thresh.copy()
        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                max_area = area
                best_cnt = cnt
            else:
                max_area = 0

        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        print "x:",cx,"y:",cy

           
        if in_rectangle(551,00,600,50,cx,cy):
            draw_color = (255,0,0)
            print "inside3"
        if in_rectangle(501,000,550,50,cx,cy):
            draw_color = (0,255,0)
            print "inside2"
        if in_rectangle(450,000,500,50,cx,cy):
            draw_color = (0,0,255)
            print "inside1"

        coor = str(cx)+","+str(cy)
        font = cv2.FONT_HERSHEY_SIMPLEX
        lineType = cv2.CV_AA

        if(abs(cx-prev_x)>100 or abs(cy-prev_y)>100):
            cv2.circle(blank_image,(cx,cy),5,draw_color,-1)
        else:
            cv2.line(blank_image,(cx,cy),(prev_x,prev_y),draw_color,3)

        img_cpy = orig_frame.copy()            
        cv2.rectangle(img_cpy,(450,000),(500,50),(255,0,0),-1) #B
        cv2.rectangle(img_cpy,(500,000),(550,50),(0,255,0),-1) #g
        cv2.rectangle(img_cpy,(550,000),(600,50),(0,0,255),-1) #r

        opacity = 0.5
        cv2.addWeighted(img_cpy, opacity, orig_frame, 1 - opacity, 0, orig_frame)

        orig_frame = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGBA)
        final = cv2.add(orig_frame,blank_image)
        final = cv2.cvtColor(final, cv2.COLOR_RGBA2BGR)
        img = Image.fromarray(final)
        cv2.imshow('thresh',thresh2)
        cv2.imshow('final',final)

            #cv2.imshow(final)

        prev_x = cx
        prev_y = cy

        k = cv2.waitKey(10)
        if k == 27:
            break

start()

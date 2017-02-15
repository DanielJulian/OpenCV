#http://stackoverflow.com/questions/14752006/computer-vision-masking-a-human-hand

import sys
import numpy
import cv2

cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, im = cap.read()
    im_ycrcb = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)

    skin_ycrcb_mint = numpy.array((0, 133, 77))
    skin_ycrcb_maxt = numpy.array((255, 173, 127))
    skin_ycrcb = cv2.inRange(im_ycrcb, skin_ycrcb_mint, skin_ycrcb_maxt)
    #cv2.imwrite(sys.argv[2], skin_ycrcb) # Second image

    contours, _ = cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area > 1000:
            cv2.drawContours(im, contours, i, (255, 0, 0), 3)
    cv2.imshow('Imagen',im)
    k = cv2.waitKey(1)
    if k == 27:
        break

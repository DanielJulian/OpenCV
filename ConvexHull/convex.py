import cv2
import numpy as np
import math



img = cv2.imread('hand.png')
img = cv2.resize(img,(800,640))
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(img_gray, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
cv2.imshow('Thresholded', thresh)

_, contours,hierarchy = cv2.findContours(thresh,2,1)
cnt = contours[0]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)
drawing = np.zeros(img_gray.shape,np.uint8)
cv2.drawContours(drawing,[cnt],0,(255,255,0),0)
cv2.imshow('thresh',thresh)
cv2.imshow('draw',drawing)
for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    #cv2.line(img,start,end,[0,255,0],2)
    #cv2.circle(img,far,5,[0,0,255],-1)

    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
    if angle <= 90:
        cv2.circle(img,far,3,[0,0,255],-1)
    #dist = cv2.pointPolygonTest(cnt,far,True)
    #cv2.line(crop_img,start,end,[0,255,0],2)
    #cv2.circle(crop_img,far,5,[0,0,255],-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import imutils
import numpy as np

cap = cv2.VideoCapture(0)
ret, img1 = cap.read()
img1 = imutils.resize(img1, width=500)

cap2 = cv2.VideoCapture("op4.mp4")
ret2, img2 = cap2.read()
img2 = imutils.resize(img2, width=500)


h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

#create empty matrix
vis = np.zeros((max(h1, h2), w1+w2,3), np.uint8)

#combine 2 images
vis[:h1, :w1,:3] = img1
vis[:h2, w1:w1+w2,:3] = img2


cv2.imshow("Image_Transformation",cv2.addWeighted(vis,0.1,vis,0.9,0))
if cv2.waitKey(0) & 0xFF == ord('q'):
    print("s2d")

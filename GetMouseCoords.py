import cv2
import numpy as np

ix,iy = -1,-1
# mouse callback function
def getCoords(event,x,y,flags,param):
    global ix,iy
    ix,iy = x,y

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',getCoords)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    print ix,iy
cv2.destroyAllWindows()

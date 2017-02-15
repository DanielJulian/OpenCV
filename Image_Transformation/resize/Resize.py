#http://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
import cv2

def start():
    cap = cv2.VideoCapture(0)
    flag, frame = cap.read()
    img2 = cv2.imread("asd.png")

    #Las transformo al mismo  size
    frame = cv2.resize(frame, (500,500), interpolation = cv2.INTER_AREA)
    img2 = cv2.resize(img2, (500,500), interpolation = cv2.INTER_AREA)
    cv2.addWeighted(frame, 0.7, img2, 1 - 0.7, 0, frame)
    cv2.imshow("fusion", frame)
    cv2.waitKey(0)

start()

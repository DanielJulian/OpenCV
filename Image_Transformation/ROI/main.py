import cv2

def start():
    cap = cv2.VideoCapture(0)
    flag, frame = cap.read()
    ROI = frame[280:340, 330:390]
    #       Y  - X
    frame[0:60, 100:160] = ROI
    cv2.imshow("Suma", frame)
    cv2.waitKey(0)

start()

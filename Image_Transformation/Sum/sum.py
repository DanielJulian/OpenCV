import cv2

def start():
    cap = cv2.VideoCapture(0)
    flag, frame = cap.read()
    img2 = cv2.imread("/home/danny/PycharmProjects/ComputerVision/OpenCV/Image_Transformation/asd.png")
    #Las transformo al mismo  size
    frame = cv2.resize(frame, (500,500), interpolation = cv2.INTER_AREA)
    img2 = cv2.resize(img2, (500,500), interpolation = cv2.INTER_AREA)
    frame = cv2.add(frame,img2)
    cv2.imshow("Suma", frame)
    cv2.waitKey(0)

start()

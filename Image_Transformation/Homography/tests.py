import cv2
import numpy as np



def start():
    webcam = cv2.VideoCapture(0)
    flag, frame = webcam.read()
    size = frame.shape

    #Puntos de la imagen origen
    pts_src = np.array(
                       [
                        [0,0], # punto del corner superior izquierdo ( X , Y )
                        [size[1] - 1, 0],  # punto del corner superior derecho( X , Y )
                        [size[1] - 1, size[0] -1], # punto del corner inferior derecho ( X , Y )
                        [0, size[0] - 1 ] # punto del corner inferior izquierdo ( X , Y )
                        ],dtype=float
                       );

    #Puntos a donde warpear la imagen
    pts_dst = np.array(
                      [
                        [0,0], # punto del corner superior izquierdo ( X , Y )
                        [size[1] - 1, 0],  # punto del corner superior derecho( X , Y )
                        [size[1] - 1, size[0] -1], # punto del corner inferior derecho ( X , Y )
                        [0, 300 ] # punto del corner inferior izquierdo ( X , Y )
                        ],dtype=float
                       );

    print pts_dst

    # Calculate Homography between source and destination points
    h, status = cv2.findHomography(pts_src, pts_dst);

    im_temp = cv2.warpPerspective(frame, h, (640,480))

    cv2.imshow("frame Original",frame)
    cv2.imshow("frame Warpeado",im_temp)

    cv2.waitKey(0) & 0xFF == ord('q')

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #   break

start()

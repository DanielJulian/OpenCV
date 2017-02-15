import cv2
import imutils
# -*- coding: utf-8 -*-

#cargamos la plantilla e inicializamos la webcam:
face_cascade = cv2.CascadeClassifier('./Cascades/haarcascade_frontalface_alt.xml')
#control_cascade = cv2.CascadeClassifier('./Cascades/cascade_guante.xml')
cap = cv2.VideoCapture(0)
while(True):
    #leemos un frame y lo guardamos
    ret, img = cap.read()
    img = imutils.resize(img, width=500)
    #convertimos la imagen a blanco y negro
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    #buscamos las coordenadas de los rostros (si los hay) y
    #guardamos su posicion
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    #control = control_cascade.detectMultiScale(gray,2,1)
    #Dibujamos un rectangulo en las coordenadas de cada rostro
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
        cv2.putText(img,'Humano',(x,y), cv2.FONT_HERSHEY_DUPLEX , 0.8,(255,255,255),2)

    #for (x,y,w,h) in control:
    #    cv2.putText(img,'Control',(x,y), cv2.FONT_HERSHEY_DUPLEX , 0.8,(255,255,255),2)

    #Mostramos la imagen
    cv2.imshow('img',img)
     
    #con la tecla 'q' salimos del programa
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

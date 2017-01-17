import cv2
import numpy as np
import os

def store_raw_images():
    path= "./original"
    neg_image_urls = [os.path.join(path, f) for f in os.listdir(path)]

    if not os.path.exists('salida'):
        os.makedirs('salida')

    for i in neg_image_urls:
        try:
            print(i)
            name = i.split("/")[2]
            img = cv2.imread(i,cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(img, (320, 243))
            cv2.imwrite("salida/"+name+".jpg",resized_image)
        except Exception as e:
            print(str(e))

store_raw_images()

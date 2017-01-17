import cv2
import os
import numpy as np

def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    # En binario, para que la salida de un xor sea 1, todas las entradas deben ser 1.
                    #https://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.bitwise_xor.html
                    # Aca comparo todos los bits de cada imagen, si son todos iguales, osea , son la misma imagen
                    #La salida es 1 = true
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

find_uglies()

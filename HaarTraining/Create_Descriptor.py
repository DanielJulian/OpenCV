import os

def create_pos_n_neg():
    for file_type in ['neg']:
        for img in os.listdir(file_type):

            if file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)


create_pos_n_neg()

#EL 1 es con 5k positivas
#Crear las samples positivas2
#opencv_createsamples -img control.jpg -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.6 -maxyangle -0.6 -maxzangle 0.6 -num 2750
# Despues el vector que describe a todas las imagenes positivas
#opencv_createsamples -info info/info.lst -num 2750 -w 20 -h 20 -vec positives.vec
#Para entrenar : opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 2600 -numNeg 1300 -numStages 10 -w 20 -h 20

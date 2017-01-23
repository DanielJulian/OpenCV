from PIL import Image
import pytesseract
words =pytesseract.image_to_string(Image.open('test.png') ,lang='deu')
print (words)

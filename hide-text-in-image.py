from stegano import lsb
from PIL import Image
import pytesseract

img = Image.open("path-to-image")

pytesseract.pytesseract.tesseract_cmd = r'path-to-tesseract'

config = '--psm 6 -l eng'
text = pytesseract.image_to_string(img, config=config)
print("Existing text in the picture")
print(text)

secret=input("Enter your secret message:")

inImage = "path-to-input-image"
outImage= "path-to-output-image"

lsb.hide(inImage,message=secret).save(outImage)

message= lsb.reveal(outImage)
print(f'Reveal message:{message}')

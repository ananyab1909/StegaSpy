from stegano import lsb
from PIL import Image


secret=input("Enter your secret message:")

inImage = "IvV2y.png"
outImage= "secret.png"

lsb.hide(inImage,message=secret).save(outImage)

message= lsb.reveal(outImage)
print(f'Reveal message:{message}')

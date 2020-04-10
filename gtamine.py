import pytesseract
from time import sleep
from PIL import ImageGrab, Image, ImageOps
import tkinter
import re
import keyboard
import mouse
def invertImage(image):
        if image.mode == 'RGBA':
                r,g,b,a = image.split()
                rgb_image = Image.merge('RGB', (r,g,b))
                inverted_image = ImageOps.invert(rgb_image)
                r2,g2,b2 = inverted_image.split()
                final_image = Image.merge('RGBA', (r2,g2,b2,a))
        else:
                final_image = ImageOps.invert(image)
        return final_image
def matchCode(s):
        return re.findall(r'[A-Z0-9] [A-Z0-9] [A-Z0-9]',s,re.M)
def pressKeys(s):
        for k in s:
                if k.isdigit():
                        keyboard.press_and_release(k)      
                else:
                        keyboard.press_and_release("shift+{}".format(k.lower()))
        sleep(5)
        for i in range(10):
                mouse.press()
                mouse.release()
                sleep(1)
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\chewb\AppData\Local\Tesseract-OCR\tesseract.exe'
i=0
root=tkinter.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
print(height, " ", width)

while True:
        quarterW=width/3
        quarterH=height/3
        #img=ImageGrab.grab(bbox=(quarterW,quarterH,quarterW+width/2,quarterH*2))
        img=ImageGrab.grab()
        img=invertImage(img)
        info=pytesseract.image_to_string(img)
        extracted=matchCode(info)
        if len(extracted)!=0:
                print(extracted)
                pressKeys(extracted[0].split(" "))
                img.save("screen{}.png".format(i))
                i+=1
        #sleep(5)

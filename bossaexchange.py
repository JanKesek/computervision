import pytesseract
from time import sleep, time
from PIL import ImageGrab, Image, ImageOps
import sys
import os
from plyer import notification
from twilio.rest import Client

log_file=open("logs.txt","w")
sys.stdout=log_file

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
def write_file(file_path,info,file_index,after_parse=0):
        if after_parse==1: file_path=file_path.format(file_index)
        else: file_path=file_path.format(file_index)+'bytes'
        with open(file_path,'w') as f:
                try:
                        if after_parse==1: print("INFO IN WRITE_FILE", info)
                        f.write(info)
                except UnicodeEncodeError as e:
                        print("UnicodeEncodeError: Cannot save file")
def read_file(file_path,file_index,after_parse=1):
        if after_parse!=1: file_path=file_path.format(file_index)+'bytes'
        else: file_path=file_path.format(file_index)       
        with open(file_path,'r') as f:
                s=f.read()
        return s
def send_sms(info):
        account_sid="ACe550a1c15a62dcaeb8aa49781f307d37"
        auth_token="7de8a0c51fbd1f3ef62823d53ac5796f"
        client=Client(account_sid,auth_token)
        message="New BOSSA news! {}".format(info)
        client.messages.create(from_='+12053868878',to='+48667876823',body=message)
def alert_new_message(file_path,info,file_index):
        if file_index!=0:
                prev_index=find_prev_newest_msg(file_index)
                prev_message=read_file(file_path,prev_index)
                if info!=prev_message:
                        notification.notify(title="New BOSSA message!",message=info)
                        #send_sms(info)
                        write_file(file_path,info,file_index,after_parse=1)
        else: write_file(file_path,info,file_index,after_parse=1)
def find_prev_newest_msg(file_index):
        while not os.path.exists("exchange\output{}.txt".format(file_index)):
                file_index-=1
        return file_index
def parse_screen_data(datain, file_index):
        datain=datain.split("\n")
        print(datain)
        #datain="\n\n".join(datain[3:7])
        datain="".join(datain[0])
        return datain
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\chewb\AppData\Local\Tesseract-OCR\tesseract.exe'
i=0

if not os.path.isdir("exchange"):
        os.makedirs("exchange")
for l in os.listdir("exchange"):
        os.remove("exchange/{}".format(l))       
while True:
        #img=ImageGrab.grab()
        img=Image.open("infoscreen.png")
        width,height=img.size
        img=img.crop((0,40,width/2, height/10))
        #img=invertImage(img)
        info=pytesseract.image_to_string(img)
        file_path='exchange/output{}.txt'
        write_file(file_path,info,i)
        s=read_file(file_path,i, after_parse=0)
        #relevantlines=s.split("\n\n")
        #relevantlines=max(relevantlines,key=len)
        #info=relevantlines.split("\n")[-1]
        infor = parse_screen_data(s,i)
        alert_new_message(file_path,infor,i)
        #write_file(file_path,info,i)        
        img.save("exchange/screen{}.png".format(i))
        #os.remove(file_path.format(i)+'bytes')
        i+=1
        sleep(2)
log_file.close()

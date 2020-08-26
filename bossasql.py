import pytesseract
from time import sleep, time
from PIL import ImageGrab, Image, ImageOps
import sys
import os
from plyer import notification
from twilio.rest import Client
import sqlite3
import datetime
import re
import tkinter as tk
import requests
import datetime
class SQLiteConn:
        @staticmethod
        def connect():
                try:
                        SQLiteConn.conn=sqlite3.connect("exchange/messages.db")
                        SQLiteConn.cursor=SQLiteConn.conn.cursor()
                        SQLiteConn.cursor.execute("""
                         CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,
                                                       hour TEXT, message TEXT)""")
                        SQLiteConn.conn.commit()
                except Exception as e:
                        print("Connection ERROR: ",e)
        @staticmethod
        def insert_message(hour,message):
                date=datetime.datetime.today().strftime('%Y-%m-%d')
                try:
                        print("BEFORE INSERT ",message)
                        SQLiteConn.cursor.execute("""
                  INSERT INTO messages(date,hour,message)
                  VALUES(?,?,?)
                """,(date,hour,message))
                        SQLiteConn.conn.commit()
                except Exception as e:
                        print("Insert ERROR: ", e)
        @staticmethod
        def delete_all():
                try:
                        SQLiteConn.cursor.execute("""delete from messages;""")
                        SQLiteConn.conn.commit()
                except Exception as e:
                        print("Delete ERROR: ",e)
        @staticmethod
        def get_last():
                SQLiteConn.cursor.execute("""
                  select hour from messages where id=(select max(id) from messages);
                """)
                rows=SQLiteConn.cursor.fetchone()
                return rows
        @staticmethod
        def get_all():
                try:
                        SQLiteConn.cursor.execute("""
                          select * from messages;
                        """)
                        rows=SQLiteConn.cursor.fetchall()
                        return rows
                except Exception as e:
                        print("select ERROR: ",e) 
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
        if type(info)!=str:
                info.save(file_path.format(file_index))
                return
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
        global twilio_keys
        account_sid,auth_token,phonenumber=twilio_keys
        client=Client(account_sid,auth_token)
        message="New BOSSA news! {}".format(info)
        client.messages.create(from_='+12053868878',to=('+48'+phonenumber),body=message)
def alert_new_message(file_path,info,file_index):
        prev_hour=find_prev_newest_msg(file_index)
        if prev_hour!=None: prev_hour=prev_hour[0]
        hour=info.split(" ")[0]
        message=" ".join(info.split(" ")[1:])
        print("PREV HOUR {} CURRENT HOUR {}".format(prev_hour,hour))
        if hour!=prev_hour:
                if is_bossa_message(info):
                        #notification.notify(title="New BOSSA message!",message=message)
                        SQLiteConn.insert_message(hour,message)
                        send_push(title=hour,message=message)      
                        #send_sms(info)
                        #write_file(file_path,info,file_index,after_parse=1)
def send_push(title,message):
        payload={'title':title,'body': message,"date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
        requests.post("https://34.68.138.17/send",json=payload,verify=False)
        #requests.post("https://localhost:3000/send",json=payload, verify=False)
def is_bossa_message(message):
        hour=message.split(" ")[0]
        print("CHECKING IF HOUR MATCHES REGEX:{}".format(hour))
        return bool(re.match(r'[0-9]{2}:[0-9]{2}',hour))
def find_prev_newest_msg(file_index):
        return SQLiteConn.get_last()
def parse_screen_data(datain, file_index):
        datain=datain.split("\n")
        print(datain)
        #datain="\n\n".join(datain[3:7])
        datain="".join(datain[0])
        return datain
def set_twilio_key(ssid,auth,phonenumber,master=None):
        global twilio_keys
        twilio_keys=[ssid,auth,phonenumber]
        with open("api.txt",'w') as f:
                f.write(' '.join([ssid,auth,phonenumber]))
        if master!=None: master.destroy()
def take_screenshot():
        imgFull=ImageGrab.grab(all_screens=True)
        #img=Image.open("infoscreen.png")
        width,height=imgFull.size
        #img=imgFull.crop((0,40,width/2, height/10))

def input_twilio_key():
        if os.path.exists("api.txt"):
                with open("api.txt",'r') as f:
                        keys=f.read().strip().split(" ")
                        set_twilio_key(keys[0],keys[1],keys[2])
        else:
                master = tk.Tk()
                tk.Label(master, text="Provide API keys to Twilio for SMS https://www.twilio.com").grid(row=0)
                tk.Label(master, text="Account SSID key: ").grid(row=1)
                tk.Label(master, text="Account auth key: ").grid(row=2)
                tk.Label(master, text="Your phone number: ").grid(row=3)
                e1 = tk.Entry(master)
                e1.grid(row=1, column=1)
                e2 = tk.Entry(master)
                e2.grid(row=2, column=1)
                e3 = tk.Entry(master)
                e3.grid(row=3, column=1)
                button=tk.Button(master, text='Confirm', 
                        command=lambda e1=e1,e2=e2,e3=e3,m=master: set_twilio_key(e1.get(), e2.get(),e3.get(),m))
                button.grid(row=3, column=0, sticky=tk.W, pady=4)
                tk.mainloop()
if __name__ == "__main__":
        #input_twilio_key()
        print("Prosze ustawic ekran na program BOSSA Nol")
        log_file=open("logs.txt","w")
        sys.stdout=log_file
        SQLiteConn.connect()
        SQLiteConn.delete_all()
        pytesseract.pytesseract.tesseract_cmd=r'C:\Users\chewb\AppData\Local\Tesseract-OCR\tesseract.exe'
        i=0
        if not os.path.isdir("exchange"):
                os.makedirs("exchange")
        #for l in os.listdir("exchange"):
        #        os.remove("exchange/{}".format(l))
        sleep(10)       
        while True:
                if i==0:
                        imgFull,img=take_screenshots()
                        write_file("exchange/fullImage{}.png",imgFull,i)
                        write_file("exchange/croppedImage{}.png",img,i)
                info=pytesseract.image_to_string(img)
                file_path='exchange/output{}.txt'
                write_file(file_path,info,i)
                s=read_file(file_path,i, after_parse=0)
                infor = parse_screen_data(s,i)
                alert_new_message(file_path,infor,i)
                os.remove(file_path.format(i)+'bytes')       
                i+=1
                sleep(2)
        log_file.close()

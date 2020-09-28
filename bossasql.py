import pytesseract
from unidecode import unidecode
from time import sleep, time
from PIL import ImageGrab, Image, ImageOps
import sys
import os
import sqlite3
import datetime
import re
import tkinter as tk
from computervision.pyrobot import Robot
#import requests
import shutil
import datetime
from computervision.mousepos import CropApp
from computervision.notifications import send_sms, set_twilio_key, input_twilio_key, send_push, send_os_notification


class SQLiteConn:
    @staticmethod
    def connect():
        if not os.path.isdir('./exchange'):
            os.makedirs("exchange") 
        try:
            dbfile=os.path.join(os.path.dirname(__file__),"exchange","messages.db")
            SQLiteConn.conn = sqlite3.connect(
               dbfile
            )
            SQLiteConn.cursor = SQLiteConn.conn.cursor()
            SQLiteConn.cursor.execute("""
                         CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,
                                                       hour TEXT, message TEXT)""")
            SQLiteConn.conn.commit()
            print("Connected to Sqlite DB at: ", dbfile)
        except Exception as e:
            print("Connection ERROR: ", e)

    @staticmethod
    def insert_message(hour, message):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        try:
            print("BEFORE INSERT ", message)
            SQLiteConn.cursor.execute("""
                  INSERT INTO messages(date,hour,message)
                  VALUES(?,?,?)
                """, (date, hour, message))
            SQLiteConn.conn.commit()
        except Exception as e:
            print("Insert ERROR: ", e)

    @staticmethod
    def delete_all():
        try:
            SQLiteConn.cursor.execute("""delete from messages;""")
            SQLiteConn.conn.commit()
        except Exception as e:
            print("Delete ERROR: ", e)

    @staticmethod
    def get_last():
        SQLiteConn.cursor.execute("""
                  select * from messages where id=(select max(id) from messages);
                """)
        rows = SQLiteConn.cursor.fetchone()
        return rows

    @staticmethod
    def get_all():
        try:
            SQLiteConn.cursor.execute("""
                          select * from messages;
                        """)
            rows = SQLiteConn.cursor.fetchall()
            return rows
        except Exception as e:
            print("select ERROR: ", e)


def write_file(file_path, info, file_index, after_parse=0):
    if type(info) != str:
        info.save(file_path.format(file_index))
        return
    if after_parse == 1:
        file_path = file_path.format(file_index)
    else:
        file_path = file_path.format(file_index)+'bytes'
    with open(file_path, 'w') as f:
        try:
            if after_parse == 1:
                print("INFO IN WRITE_FILE", info)
            f.write(info)
        except UnicodeEncodeError as e:
            print("UnicodeEncodeError: Cannot save file")


def read_file(file_path, file_index, after_parse=1):
    if after_parse != 1:
        file_path = file_path.format(file_index)+'bytes'
    else:
        file_path = file_path.format(file_index)
    with open(file_path, 'r') as f:
        s = f.read()
    return s


def alert_new_message(info):
    prev_hour = find_prev_newest_msg()
    if prev_hour != None:
        #WYJASNIENIE 3 TO TEKST WIADOMOSCI, 2 TO GODZINA
        prev_hour = prev_hour[3]
        print("PREV MESSAGE",prev_hour)
    hour = info.split(" ")[0]
    message = " ".join(info.split(" ")[1:])
    #print("PREV HOUR {} CURRENT HOUR {}".format(prev_hour, hour))
    if message != prev_hour:
        print(message)
        if is_bossa_message(hour):
            #notification.notify(title="New BOSSA message!",message=message)
            message=unidecode(message)
            send_os_notification(hour, message)
            SQLiteConn.insert_message(hour, message)
            print("New message found sending message")
            return True
            # send_push(title=hour,message=message)
            # send_sms(info)
            # write_file(file_path,info,file_index,after_parse=1)
    return False

def is_bossa_message(hour):
    #hour = message.split(" ")[0]
    #print("CHECKING IF HOUR MATCHES REGEX:{}".format(hour))
    return bool(re.match(r'[0-9]{2}:[0-9]{2}', hour))


def find_prev_newest_msg():
    return SQLiteConn.get_last()


def parse_screen_data(datain):
    datain2 = datain.split("\n")
    print(datain)
    # datain="\n\n".join(datain[3:7])
    datain2 = "".join(datain2[0])
    return datain, datain2

# FUNCTION RETURNS: FULL IMAGE, CROPPED IMAGE, IMAGE COORDINATES

def read_text_from_image(img):
    return unidecode(pytesseract.image_to_string(img))
def crop_screenshot(xy, imgFull):
    if len(xy) == 0:
        #print("BEFORE CROP", imgFull)
        crop = CropApp(imgFull)
        #print("AFTER CROP")
        xy = crop.xy
        #print(xy)
    #print("OUR COORDINATES AFTER CROP: ", xy)
    # img=imgFull.crop((38,3,1012,505))\
    #imgFull = Image.open(filepath)
    img = imgFull.crop((xy['x1'], xy['y1'], xy['x2'], xy['y2']))
    return img, xy
    # img=Image.open("infoscreen.png")
    #img=imgFull.crop((0,40,width/2, height/10))


def take_input_number(monitors):
    print("Wybierz numer monitora 1-n (domyslnie 1)")
    try:
        monitor_index = input()
        if len(monitor_index)==0: return 1
        monitor_index=int(monitor_index)
    except:
        print("Numer monitora to musi byc liczba. Wybrana domyslna opcja (1)")
        return 1
    if monitor_index > len(monitors):
        print("""Masz za malo monitorow aby wybrac {}, dostepne
                        1-{}. Wybrana domyslna opcja (1)""".format(monitor_index, len(monitors)))
        return 1
    return monitor_index


def take_input_list():
    imgCrop={}
    print("""Wpisz 4 wspolrzedne wycinka [x1,y1,x2,y2],
                lub enter (jesli chcesz wyciac przez aplikacje)""")
    try:
        crops=input()
        if len(crops)==0: return imgCrop
        crops=crops.split(" ")
        cropList=list(map(int,crops))
        for i,key in enumerate(['x1','y1','x2','y2']):
            imgCrop[key]=cropList[i]
        return imgCrop
    except Exception as e:
        print("Zle wpisales wspolrzedne ", e)
        return {}
def take_screenshot(robot,monitor):
    return robot.take_screenshot(monitor)
def take_input(robot):
    monitors = robot.get_display_monitors()
    monitor_index = take_input_number(monitors)
    #fullImg = robot.take_screenshot(monitors[monitor_index-1])
    imgcrop = take_input_list()
    return imgcrop,monitors[monitor_index-1]
def connect_db():
    SQLiteConn.connect()
    #SQLiteConn.delete_all()
if __name__ == "__main__":
    # input_twilio_key()
    print("Prosze ustawic ekran na program BOSSA Nol")
    connect_db()
    if shutil.which("tesseract") is None:
        print("Trzeba ustawic sciezke do tesseract.exe")
        pytesseract.pytesseract.tesseract_cmd=r'C:\Users\Pawel\AppData\Local\Tesseract-OCR\tesseract.exe'
    i = 0
    if not os.path.isdir("exchange"):
        os.makedirs("exchange")
    # for l in os.listdir("exchange"):
    #    os.remove("exchange/{}".format(l))
    robot=Robot()
    xycrop, monitor = take_input(robot)
    if len(xycrop)==0: print("PRosze KLIKNAC 2 KROTNIE (WYBRAC WSPOLRZEDNE CROPA)")
    log_file = open("logs.txt", "w")
    sys.stdout = log_file

    sleep(1)
    while True:
        # FUNCTION RETURNS: FULL IMAGE, CROPPED IMAGE, IMAGE COORDINATES
        # imgFull=ImageGrab.grab(all_screens=True)
        start_time = time()
        imgFull=take_screenshot(robot,monitor)
        full_img_path = "exchange/fullImage{}.png"
        cropped_img_path = "exchange/croppedImage{}.png"
        #img, xycrop = crop_screenshot(full_img_path.format(i), xycrop, imgFull)
        img, xycrop = crop_screenshot(xycrop, imgFull)
        if i==0: 
            print(xycrop, img)
            write_file(full_img_path, imgFull, i)
            write_file(cropped_img_path, img, i)
        #if i != 0:
        #    os.remove(full_img_path.format(i))
        #    os.remove(cropped_img_path.format(i))
        info = read_text_from_image(img)
        #file_path = 'exchange/output{}.txt'
        #write_file(file_path, info, i)
        #s = read_file(file_path, i, after_parse=0)
        #info2,info=parse_screen_data(info)
        #print("PARSED TEXT: ",info)
        msg_found=alert_new_message(info)
        #os.remove(file_path.format(i)+'bytes')
        i += 1
        if msg_found:
            print("MESSAGE FOUND IN --- %s seconds ---" % (time() - start_time))
    log_file.close()

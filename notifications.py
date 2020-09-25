import datetime
import requests
from plyer import notification
from playsound import playsound
import os
#from twilio.rest import Client


def send_sms(info):
        global twilio_keys
        account_sid,auth_token,phonenumber=twilio_keys
        client=Client(account_sid,auth_token)
        message="New BOSSA news! {}".format(info)
        client.messages.create(from_='+12053868878',to=('+48'+phonenumber),body=message)

def set_twilio_key(ssid,auth,phonenumber,master=None):
        global twilio_keys
        twilio_keys=[ssid,auth,phonenumber]
        with open("api.txt",'w') as f:
                f.write(' '.join([ssid,auth,phonenumber]))
        if master!=None: master.destroy()
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
def send_push(title,message):
        payload={'title':title,'body': message,"date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
        requests.post("https://34.68.138.17/send",json=payload,verify=False)
        return
        #requests.post("https://localhost:3000/send",json=payload, verify=False)

def send_os_notification(title,message):
        notification.notify(title=title,message=message)
        beepfilepath=os.path.join(os.path.dirname(os.path.realpath(__file__)),"beeps","beep-05.mp3")
        print(beepfilepath)
        playsound(beepfilepath)
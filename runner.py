from time import sleep
import os
def readFile():
    with open('logs.txt','r') as f:
        lines=f.readlines()
    return lines[-1]
def isLine(line):
    if line == "CreateCompatibleBitmap Failed because of CompatibleDC\n":
        return True
    if line == "CreateCompatibleBitmap Failed Because of bitmap\n":
        return True
if 'logs.txt' in os.listdir(): os.remove("logs.txt")
if 'bossa_params.json' in os.listdir(): os.remove("bossa_params.json")
while True:
    if 'logs.txt' in os.listdir():
        line=readFile()
        if isLine(line):
            os.system("python -m computervision.bossasql")
    else:
        os.system("python -m computervision.bossasql")
    sleep(10)
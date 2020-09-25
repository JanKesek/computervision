import pytest
from ..bossasql import take_screenshot, crop_screenshot, take_input, parse_screen_data, read_text_from_image
from ..pyrobot import Robot
import pytesseract
import os
from .. import bossasql
import PIL
def test_take_input():
    robot=Robot()
    imgcrop,monitor = take_input(robot)
    print(monitor)
    assert len(monitor)==4 and type(monitor)==tuple 
def test_cropped_screenshot_dimmensions():
    robot=Robot()
    imgFull=take_screenshot(robot,(0, 0, 1366, 768))
    img, xycrop = crop_screenshot({'x1':0,'y1':0,'x2':300,'y2':250}, imgFull)
    assert img.width==300 and img.height==250
def test_parse_message():
    img=PIL.Image.open(os.path.join(os.path.dirname(bossasql.__file__),"exchange","croppedImage0.png"))
    info=pytesseract.image_to_string(img)
    datain,dataout=parse_screen_data(info)
    assert datain==dataout
def test_parse_message_consistent():
    msgs=[]
    for i in range(10):
        img=PIL.Image.open(os.path.join(os.path.dirname(bossasql.__file__),"exchange","croppedImage0.png"))
        info=read_text_from_image(img)
        msgs.append(info)
    assert len(set(msgs))==1
    #assert type(img)==PIL.PngImagePlugin.PngImageFile
    #info=pytesseract.image_to_string(img)
    
#def test_cropped_image_has_correct_dimmensions():

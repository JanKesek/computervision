import pytest
from ..bossasql import take_screenshot, crop_screenshot, take_input
from ..pyrobot import Robot
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
#def test_cropped_image_has_correct_dimmensions():

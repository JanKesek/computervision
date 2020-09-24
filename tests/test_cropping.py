import pytest
from ..bossasql import take_screenshot, crop_screenshot, take_input

def test_take_input():
    imgcrop,monitor = take_input()
    print(monitor)
    assert len(monitor)==4 and type(monitor)==tuple 
#def test_cropped_image_has_correct_dimmensions():

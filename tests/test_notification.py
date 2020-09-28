import pytest
from ..notifications import send_os_notification
from ..bossasql import read_text_from_image, alert_new_message, connect_db
from .. import bossasql
import PIL
import os

def test_os_notification():
    send_os_notification("title","message")

def test_alert_once_on_two_same():
    connect_db()
    results=[]
    for i in range(2):
        img=PIL.Image.open(os.path.join(os.path.dirname(bossasql.__file__),"exchange","croppedImage0.png"))
        msg=read_text_from_image(img)
        results.append(alert_new_message(msg))
    assert results[0] and not results[1]
def test_alert_twice_on_same_time():
    results=[alert_new_message(read_text_from_image(PIL.Image.open(
        os.path.join(os.path.dirname(__file__),"croppedImage%s.png" % i)
    ))) for i in range(2)]
    assert results[0] and results[1]
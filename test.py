from rotary import rotaryenc
from EbOled import EbOled
import time

# OLED
oled = EbOled()
oled.begin()
oled.clear()
oled.display()

value = 0

def callback(r):
    global value
    value += r
    oled.drawString('value=' + str(value))
    oled.display()

re = rotaryenc()
re.registerCallback(callback)
try:
    time.sleep(120)
except KeyboardInterrupt:
    pass
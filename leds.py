# -*- coding: utf-8 -*-
from entryboard import *
import time
import RPi.GPIO as GPIO

# LEDが接続されているGPIOのリスト
leds = [LED1, LED2, LED3 ,LED4]

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

for i in range(10):
        for l in leds:
                GPIO.output(l, 1)
                time.sleep(1)
                GPIO.output(l, 0)
GPIO.cleanup(leds)

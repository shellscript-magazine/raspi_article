# -*- coding: utf-8 -*-
from entryboard import *
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
bz = GPIO.PWM(BUZZER, 1000)

bz.start(50)
time.sleep(2)
bz.stop()
GPIO.cleanup(BUZZER)
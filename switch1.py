# -*- coding: utf-8 -*-
from entryboard import *
import time
import sys
import RPi.GPIO as GPIO

switches = [SW1, SW2, SW3, SW4]
leds = [LED1, LED2, LED3, LED4]
GPIO.setmode(GPIO.BCM)
# スイッチのGPIOを入力に設定
GPIO.setup(switches, GPIO.IN)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

try:
        while True:
                for i in range(4):
                        if GPIO.input(switches[i]) == GPIO.LOW:
                                GPIO.output(leds[i], GPIO.HIGH)
                        else:
                                GPIO.output(leds[i], GPIO.LOW)

except KeyboardInterrupt:
        GPIO.cleanup(switches)
        GPIO.cleanup(leds)
        sys.exit()

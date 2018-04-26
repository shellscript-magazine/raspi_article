# -*- coding: utf-8 -*-
from entryboard import *
import time
import pigpio

gpio = pigpio.pi()
gpio.set_mode(BUZZER, pigpio.OUTPUT)
gpio.hardware_PWM(BUZZER, 1000, 500000) # 1kHz, 50%
time.sleep(2)
gpio.hardware_PWM(BUZZER,0 ,0)
gpio.stop()

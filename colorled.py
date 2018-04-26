# -*- coding: utf-8 -*-
from entryboard import *
import time
import RPi.GPIO as GPIO

led5 = [LED6_R, LED6_G, LED6_B]
duty = [50.0, 50.0, 50.0]
switches = [SW1, SW2, SW3, SW4]
pwm = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(led5, GPIO.OUT)
GPIO.setup(switches, GPIO.IN)

for i in range(3):
        # 100Hzに設定
        pwm.append(GPIO.PWM(led5[i], 100))
        pwm[i].start(duty[i])
try:
        while True:
                for i in range(3):
                        if GPIO.input(switches[i]) == GPIO.LOW:
                                if GPIO.input(SW4) == GPIO.LOW:
                                        duty[i] = duty[i] - 5.0
                                        if duty[i] < 0.0:
                                                duty[i] = 0.0
                                else:
                                        duty[i] = duty[i] + 5.0
                                        if duty[i] > 100.0:
                                                duty[i] = 100.0
                        pwm[i].ChangeDutyCycle(duty[i])
                        time.sleep(0.1)
except KeyboardInterrupt:
        GPIO.cleanup()

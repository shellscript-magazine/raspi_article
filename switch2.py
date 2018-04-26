# -*- coding: utf-8 -*-
from entryboard import *
import time
import sys
import RPi.GPIO as GPIO

switches = [SW1, SW2, SW3, SW4]
leds = [LED1, LED2, LED3, LED4]

# スイッチのGPIOが変化したらこの関数が呼ばれる
def switch_event(channel):
        global leds
        global switches

        for i in range(4):
                if channel == switches[i]:
                        if GPIO.input(channel) == GPIO.LOW:
                                GPIO.output(leds[i], GPIO.HIGH)
                        else:
                                GPIO.output(leds[i], GPIO.LOW)

# スクリプトはここから始まります
if __name__ == "__main__":

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switches, GPIO.IN)
        GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

        for i in range(4):
		# イベントを登録する
                GPIO.add_event_detect(switches[i], GPIO.BOTH, bouncetime=60)
                GPIO.add_event_callback(switches[i], switch_event)

        try:
		# 1時間何もしない
                time.sleep(3600)

        except KeyboardInterrupt:
                GPIO.cleanup(switches)
                GPIO.cleanup(leds)
                sys.exit()

# -*- coding: utf-8 -*-
from entryboard import *
import time
import pigpio

# 1オクターブの音階周波数リスト
scale = [ 523.251, 587.33, 659.255, 698.456, 783.991, 880, 987.767, 1046.502 ]
switches = [SW1, SW2, SW3, SW4]

bouncetime = 5 *1000 # 5ms
prev_tick = 0

# コールバック
def switch_event(channel, edge, tick):
        global bouncetime
        global prev_tick
        global scale
        global switches

        if (tick-prev_tick) < bouncetime:
                return
        prev_tick = tick

        for i in range(4):
                if switches[i] == channel:
                        if edge == pigpio.LOW:
                                gpio.hardware_PWM(BUZZER, scale[i], 500000)
                        else:
                                gpio.hardware_PWM(BUZZER, 0, 0)

if __name__ == "__main__":
        gpio = pigpio.pi()
        gpio.set_mode(BUZZER, pigpio.OUTPUT)
        for i in range(4):
                # モードとコールバック
                gpio.set_mode(switches[i], pigpio.INPUT)
                gpio.callback(switches[i], pigpio.EITHER_EDGE, switch_event)
        try:
                time.sleep(3600)
        except KeyboardInterrupt:
                gpio.hardware_PWM(BUZZER, 0, 0)
                gpio.stop()
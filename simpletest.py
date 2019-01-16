#!/usr/bin/env python3
import time
from  VCNL4020 import  VCNL4020

sensor = VCNL4020()

# コールバック関数
def callback(lux, prox):
	print('センサーに何かが接近しています')
	print('現在の明るさ:'+str(lux) )
	print('近接センサー:'+str(prox) )
	# 割り込み再設定
	sensor.enable_interrupt(callback)


# しきい値高を設定
sensor.set_high_threshold(2500)
# しきい値低を設定
sensor.set_low_threshold(0)
# 割り込み有効化
sensor.enable_interrupt(callback)

try:
	while True:
		time.sleep(1)
		

except KeyboardInterrupt:
	term = True

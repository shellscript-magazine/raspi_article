#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tsl2561 import TSL2561
from OLED import OLED
import time

oled = OLED()
# アドレスを指定する
tsl = TSL2561(address=0x29)

oled.put_string('Current LUX')

while True:
	# lux()メソッドで現在の照度を得ることが出来る
	oled.put_string(str(tsl.lux()), 1)
	time.sleep(1)
# -*- coding: utf-8 -*-
# etnryboard.pyを読み込む
from entryboard import *
import time
import RPi.GPIO as GPIO

# 動作モード設定
GPIO.setmode(GPIO.BCM)
# GPIOモード設定
GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
# LED1に１を出力
GPIO.output(LED1, GPIO.HIGH)
# 2秒待つ
time.sleep(2)
# LED1に0を出力
GPIO.output(LED1, GPIO.LOW)
# 終了処理
GPIO.cleanup(LED1)

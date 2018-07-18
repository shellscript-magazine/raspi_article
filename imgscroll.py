#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class EB_OLED(Adafruit_SSD1306.SSD1306_128_64):

	WIDTH = 128
	HEIGHT = 64
	
	__RST = 24
	__DC = 23
	SPI_PORT = 0
	SPI_DEVICE = 0
	
	def __init__(self):
		self.__spi = SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=8000000)
		super().__init__(rst=self.__RST, dc=self.__DC, spi=self.__spi)


SW1=4
SW2=17
SW3=5
SW4=6

pos_y = 0
img_height = 0
f_exit = False
jpg = None

def sw_event(channel):

	global pos_y
	global f_exit
	global jpg
	global img_height

	if channel == SW1:
		if (img_height - pos_y - EB_OLED.HEIGHT) >= 0:
			pos_y += 1
	elif channel == SW4:
		if pos_y <= 0:
			return
		pos_y -= 1
	elif channel == SW2:
		f_exit = True
	
	image = jpg.crop(box=(0, pos_y, EB_OLED.WIDTH, EB_OLED.HEIGHT+pos_y))
	oled.image(image)
	oled.display()
	

if __name__ == "__main__":

	oled = EB_OLED()
	# OLED 初期化
	oled.begin()
	oled.clear()
	oled.display()
	
	# スイッチ初期化
	GPIO.setmode(GPIO.BCM)
	GPIO.setup([SW1, SW2, SW4], GPIO.IN)
	GPIO.add_event_detect(SW1, GPIO.FALLING, bouncetime=60)
	GPIO.add_event_detect(SW2, GPIO.FALLING, bouncetime=60)
	GPIO.add_event_detect(SW4, GPIO.FALLING, bouncetime=60)
	
	GPIO.add_event_callback(SW1, sw_event )
	GPIO.add_event_callback(SW2, sw_event )
	GPIO.add_event_callback(SW4, sw_event )
	
	jpg = Image.open("sample.jpg")
	scale = float(float(EB_OLED.WIDTH)/float(jpg.size[0]))
	jpg = jpg.resize((int(jpg.size[0] * scale), int(jpg.size[1]*scale)))
	# 2値に変換
	jpg = jpg.convert('1')
	img_height = jpg.size[1]
	
	image = jpg.crop(box=(0, 0, EB_OLED.WIDTH, EB_OLED.HEIGHT))
	oled.image(image)
	oled.display()

	while f_exit == False:
		time.sleep(0.1)

	GPIO.cleanup()
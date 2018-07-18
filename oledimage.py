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


if __name__ == "__main__":

	oled = EB_OLED()
	# 初期化
	oled.begin()
	oled.clear()
	oled.display()
	
	jpg = Image.open("sample.jpg")
	# 画像を縮小
	scale = float(float(EB_OLED.WIDTH)/float(jpg.size[0]))
	jpg = jpg.resize((int(jpg.size[0] * scale), int(jpg.size[1]*scale)))
	jpg = jpg.crop(box=(0, 0, EB_OLED.WIDTH, EB_OLED.HEIGHT))
	# 2値に変換
	image = jpg.convert('1')
	oled.image(image)
	oled.display()
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# OLEDのサイズ設定
OLED_WIDTH = 128
OLED_HEIGHT = 64

# OLEDとSPIバスの設定
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# フォントの設定
DEFAULT_FONT = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
FONT_SIZE = 14


# SPIオブジェクト
spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000)

# 128×64ドットのOLEDオブジェクト
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=spi)

# OLEDオブジェクトのスタート
disp.begin()

# OLEDオブジェクトのバッファクリア
disp.clear()
# バッファの表示
disp.display()

# Imageオブジェクトの作成
image = Image.new('1', (OLED_WIDTH, OLED_HEIGHT) ,0)

# drawオブジェクトの取得
draw = ImageDraw.Draw(image)

# TryeTypeフォントオブジェクト
jpfont = ImageFont.truetype(DEFAULT_FONT, FONT_SIZE, encoding='unic')

# 文字をimageに描く
draw.text((0,0), 'こんにちは', font=jpfont, fill=1)
draw.text((0,16), 'Hello, World', font=jpfont, fill=1)
draw.text((0,32), 'シェルスクリプトマガジン', font=jpfont, fill=1)
draw.text((0,48), 'ラズパイ入門ボード', font=jpfont, fill=1)

# imageをOLEDバッファに書き込む
disp.image(image)
# バッファを表示
disp.display()

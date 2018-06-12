import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class OLED():
	OLED_WIDTH = 128
	OLED_HEIGHT = 64

	RST = 24
	DC = 23
	SPI_PORT = 0
	SPI_DEVICE = 0

	DEFAULT_FONT = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
	FONT_SIZE = 14
	
	_LINE_HEIGHT = 16

	def __init__(self, port=SPI_PORT, dev=SPI_DEVICE, _rst=RST, _dc=DC):
		self._spi = SPI.SpiDev(port, dev, max_speed_hz=8000000)
		self._disp = Adafruit_SSD1306.SSD1306_128_64(rst=_rst, dc=_dc, spi=self._spi)
		self._disp.begin()
		self._disp.clear()
		self._disp.display()
		self._image = Image.new('1', (self.OLED_WIDTH, self.OLED_HEIGHT) ,0)
		self._draw = ImageDraw.Draw(self._image)
		self._font = ImageFont.truetype(self.DEFAULT_FONT, self.FONT_SIZE, encoding='unic')
		
	def put_string(self, str, line=0):
		self._draw.rectangle((0, line*self._LINE_HEIGHT, self.OLED_WIDTH,line*self._LINE_HEIGHT+self._LINE_HEIGHT), fill=(0))
		self._draw.text((0, line*self._LINE_HEIGHT), str, font=self._font, fill=1)
		self._disp.image(self._image)
		self._disp.display()
		

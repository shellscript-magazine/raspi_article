import smbus
import time
import RPi.GPIO as GPIO
from threading import BoundedSemaphore

class VCNL4020():

	_ALS_OD       = 0b00010000	# オンデマンド明るさ計測スタート
	_PROX_OD      = 0b00001000	# オンデマンド近接計測スタート
	_ALS_EN       = 0b00000100	# 明るさ繰り返し計測有効
	_PROX_EN      = 0b00000010	# 近接繰り返し計測有効
	_SELFTIMED_EN = 0b00000001	# 内蔵タイマー有効
	
	_CONT_CONV    = 0b10000000	# Continue Conversion有効
	_AMBIENT_RATE = 0b00010000	# 明るさの計測レート（default:2sample/s）
	_AUTO_OFFSET  = 0b00001000	# 自動オフセットモード有効
	_AVERAGING    = 0b00000101	# 平均化（default:32conv）
	
	_COMMAND_REG       = 0x80	# コマンドレジスタ
	_PID_REG           = 0x81	# プロダクトIDレジスタ
	_PROX_RATE_REG     = 0x82	# 近接測定レートジスタ
	_IR_CURRENT_REG    = 0x83	# 近接測定用赤外線LED電流設定レジスタ（default=20mA）
	_AMBIENT_PARAM_REG = 0x84	# 明るさセンサーパラメータレジスタ
	
	_AMBIENT_MSB       = 0x85	# 明るさ上位バイト
	_AMBIENT_LSB	   = 0x86	# 明るさ下位バイト
	
	_PROX_MSB          = 0x87	# 近接上位バイト
	_PROX_LSB          = 0x88	# 近接下位バイト
	
	_INT_CONTROL_REG   = 0x89	# 割り込み制御レジスタ
	
	_LOW_TH_MSB		   = 0x8A	# Lowしきい値（MSB）
	_LOW_TH_LSB		   = 0x8B	# Lowしきい値（LSB）
	_HIGH_TH_MSB	   = 0x8C   # Highしきい値（MSB）
	_HIGH_TH_LSB	   = 0x8D	# Highしきい値（LSB）
	
	_INT_STATUS_REG	   = 0x8E	# 割り込みステータス
	
	_INT_NO			   = 0x06	# int = GPIO6
	
	# コールバック
	__callbackfunc	   = None
	
	def __init__(self, i2c_addr = 0x13, busno = 1):
		self.addr = i2c_addr
		self.i2c = smbus.SMBus(busno)
		
		self._write_reg(self._COMMAND_REG, self._ALS_OD  |\
										   self._PROX_OD |\
										   self._ALS_EN  |\
										   self._PROX_EN |\
										   self._SELFTIMED_EN )
										   
		self._write_reg(self._IR_CURRENT_REG, 2 )	# 20mA
										   
		self._write_reg(self._AMBIENT_PARAM_REG, self._CONT_CONV    |\
												 self._AMBIENT_RATE |\
												 self._AUTO_OFFSET  |\
												 self._AVERAGING )
		self.semaphore = BoundedSemaphore()

		# GPIO設定
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self._INT_NO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self._INT_NO, GPIO.FALLING, callback=self.__interruptfunc)
		
		time.sleep(0.6)			# 初回測定まで待つ
		
	def _write_reg(self, reg, value):
		self.i2c.write_byte_data(self.addr, reg, value)
	
	def _read_reg(self, reg):
		return self.i2c.read_byte_data(self.addr, reg)
	
	# 高値用レジスタ設定
	def set_high_threshold(self, value):
		self.semaphore.acquire()
		h = (value & 0xFF00) >> 8
		l = value & 0x00FF
		self._write_reg(self._HIGH_TH_MSB, h)
		self._write_reg(self._HIGH_TH_LSB, l)
		self.semaphore.release()
	
	# 低値用レジスタ設定
	def set_low_threshold(self, value):
		self.semaphore.acquire()
		h = (value & 0xFF00) >> 8
		l = value & 0x00FF
		self._write_reg(self._LOW_TH_MSB, h)
		self._write_reg(self._LOW_TH_LSB, l)
		self.semaphore.release()
	
	# 割り込み有効化
	def enable_interrupt(self, callbackfunc=None, prox=True, samples=1):
		self.semaphore.acquire()

		self.__callbackfunc = callbackfunc
		value = self._read_reg(self._INT_CONTROL_REG)
		
		if callbackfunc is not None:
			if prox:
				value |= 0b00000010
			else:
				value |= 0b00000011
		else:
				value &= 0b11111100
	
		# samples
		samples &= 0b00000111
		samples = samples << 5
		value &= 0b00011111
		value |= samples
		
		self._write_reg( self._INT_CONTROL_REG, value)
		self.semaphore.release()
	
	# 割り込み関数
	def __interruptfunc(self, ch):
		if ch != self._INT_NO:
			return
		if self.__callbackfunc is not None:
			self.__callbackfunc(self.luminance, self.proximity)
		
	
	@property
	def luminance(self):
		self.semaphore.acquire()
		d = self.i2c.read_i2c_block_data(self.addr, self._AMBIENT_MSB, 2)
		self.semaphore.release()
		return (d[0] * 256 + d[1]) / 4
	
	@property
	def proximity(self):
		self.semaphore.acquire()
		d = self.i2c.read_i2c_block_data(self.addr, self._PROX_MSB, 2)
		self.semaphore.release()
		return (d[0] * 256 + d[1])

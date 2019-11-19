import time
import smbus2
import bme280
from led4digits import LED4DIGITS

BME280_ADDR = 0x76
BUS_NO = 1

# BME280
i2c = smbus2.SMBus(BUS_NO)
bme280.load_calibration_params(i2c, BME280_ADDR)

# LED Start
led = LED4DIGITS()
led.start() # 点灯開始

try:
    while True:
      data = bme280.sample(i2c, BME280_ADDR)
      led.print(data.temperature)
      time.sleep(1)
except KeyboardInterrupt:
    led.stop()

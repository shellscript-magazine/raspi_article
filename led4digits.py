from mcpgpio import MCPGPIO
import threading
import time

class LED4DIGITS(threading.Thread):

  # 点灯させる桁のコード
  __dig = [
    [0b00000000, 0b00100000], #13
    [0b00010000, 0b00000000], #4
    [0b00001000, 0b00000000], #3
    [0b00000100, 0b00000000]  #2
  ]

  # ドットのコード
  __dot = [0b00000000, 0b00000100] # 10

  # 数値のコード
  __leds = [ [0b11100000, 0b00001011 ],  # [7, 5, 11, 9, 8, 6] 
           [0b00100000, 0b00001000 ],  # [5, 11] 
           [0b10100000, 0b00010011 ],  # [7, 5, 12, 8, 9]
           [0b10100000, 0b00011010 ],  # [7, 5, 12, 11, 9]
           [0b01100000, 0b00011000 ],  # [6, 12, 5, 11]
           [0b11000000, 0b00011010 ],  # [7, 6, 12, 11, 9]
           [0b11000000, 0b00011011 ],  # [7, 6, 12, 11, 9, 8]
           [0b10100000, 0b00001000 ],  # [7, 5, 11]
           [0b11100000, 0b00011011 ],  # [7, 5, 11, 9, 8, 6, 12]
           [0b11100000, 0b00011010 ]   # [7, 5, 11, 9, 6, 12]
    ]

  __d = 0                 # 現在の桁
  value = 0               # 表示する値
  __term = False          # 停止フラグ
  __p = -1                # ドットの位置

  def __init__(self):
    threading.Thread.__init__(self)

    self.gpio = MCPGPIO()

    for i in range(16):
      self.gpio.setup(i, self.gpio.OUTPUT)
      self.gpio.output(i, self.gpio.LOW)

  def print(self, v):
    if (v > 9999) or (v < 0):
      return

    self.__p = -1
    self.value = 0
    if isinstance(v, int):
      self.value = v

    elif isinstance(v, float):
      s = '{:.4g}'.format(v)
      if float(s) < 10:
        self.value = int(float(s) * 1000)
        self.__p = 3
      elif float(s) < 100:
        self.value = int(float(s) * 100)
        self.__p = 2
      elif float(s) < 1000:
        self.value = int(float(s) * 10)
        self.__p = 1
      else:
        self.value = int(s)

    else:
      return
    
  def stop(self):
    self.__term = True

  def run(self):
    while not self.__term:
      d = self.__d & 0b11
      co = 10 ** d
      n = int(self.value / co)
      p = int(n / 10)
      n %= 10
      # clear
      self.gpio.gpioa = 0
      self.gpio.gpiob = 0
      if (n != 0) or (d == 0) or (p > 0) or (self.__p == 3):
        # put
        a = self.__leds[n][0] | self.__dig[d][0]
        b = self.__leds[n][1] | self.__dig[d][1]
        if self.__p == d:
          a |= self.__dot[0]
          b |= self.__dot[1]
        self.gpio.gpioa = a
        self.gpio.gpiob = b

      self.__d += 1
      time.sleep(0.002)
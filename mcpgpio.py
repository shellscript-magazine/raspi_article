from smbus import SMBus

class MCPGPIO():
  __IODIR  = [0x00, 0x01] # レジスタ番号
  __GPPU   = [0x0C, 0x0D]
  __GPIO   = [0x12, 0x13]
  __OLAT   = [0x14, 0x15]

  INPUT       = 1
  OUTPUT      = 0
  INPUTPULLUP = 3

  HIGH        = 1
  LOW         = 0

  def __init__(self,address = 0x20):
    self.bus = SMBus(1)
    self.addr = address

  def setup(self, pin, dir):
    if pin < 16:
      dir = self.bus.read_byte_data(self.addr,self.__IODIR[int(pin/8)])
      dir &= ~(0x01 << int(pin % 8))
      dir |= (dir & 1) << int(pin % 8)
      self.bus.write_byte_data(self.addr, self.__IODIR[int(pin/8)], dir)
      if (dir & 1) ==  1:
        pu  = self.bus.read_byte_data(self.addr,self.__GPPU[int(pin/8)])
        pu &= ~(0x01 << int(pin % 8))
        pu |= ((dir >> 1) & 1) << int(pin % 8)
        self.bus.write_byte_data(self.addr, self.__GPPU[int(pin/8)], pu)
    
  def input(self, pin):
    r = 0
    if pin < 16:
      gp = self.bus.read_byte_data(self.addr, self.__GPIO[int(pin/8)])
      r = (gp >> int(pin%8) & 1)
    return r

  def output(self, pin, val):
    if pin < 16:
      gp = self.bus.read_byte_data(self.addr, self.__GPIO[int(pin/8)])
      gp &= ~(0x01 << int(pin % 8))
      gp |= (val & 1) << int(pin % 8)
      self.bus.write_byte_data(self.addr, self.__GPIO[int(pin/8)], gp)

  @property
  def gpioa(self):
    return  self.bus.read_byte_data(self.addr, self.__GPIO[0])
    
  @gpioa.setter
  def gpioa(self, value):
    self.bus.write_byte_data(self.addr,self.__GPIO[0], value)
    
  @property
  def gpiob(self):
    return  self.bus.read_byte_data(self.addr, self.__GPIO[1])

  @gpiob.setter
  def gpiob(self, value):
    self.bus.write_byte_data(self.addr,self.__GPIO[1], value)
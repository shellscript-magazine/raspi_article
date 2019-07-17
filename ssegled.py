from mcpgpio import MCPGPIO

class LED7SEG():
    __leds = [  [0, 1, 2, 8, 9, 10],    # 0
                [2, 8],                 # 1
                [9, 8, 11, 0, 1],       # 2
                [9, 8, 11, 2, 1],       # 3
                [10,11, 2, 8],          # 4
                [9, 10, 11, 2, 1],      # 5
                [9, 10, 11, 2, 1, 0],   # 6
                [9, 8, 2],              # 7
                [0, 1, 2, 8, 9, 10, 11],# 8
                [1, 2, 8, 9, 10, 11]    # 9
            ]

    def __init__(self):
        self.gpio = MCPGPIO()
        self.gpio.setup(0, MCPGPIO.OUTPUT)
        self.gpio.setup(1, MCPGPIO.OUTPUT)
        self.gpio.setup(2, MCPGPIO.OUTPUT)
        self.gpio.setup(3, MCPGPIO.OUTPUT)
        self.gpio.setup(8, MCPGPIO.OUTPUT)
        self.gpio.setup(9, MCPGPIO.OUTPUT)
        self.gpio.setup(10, MCPGPIO.OUTPUT)
        self.gpio.setup(11, MCPGPIO.OUTPUT)

    def off(self):
        for l in self.__leds[8]:
            self.gpio.output(l, MCPGPIO.LOW)
    
    def print(self, n):
        if (n < 0) or (n > 9):
            return
        
        self.off()
        for l in self.__leds[n]:
            self.gpio.output(l, MCPGPIO.HIGH)

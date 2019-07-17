from ssegled import LED7SEG
import time

led = LED7SEG()

for i in range(10):
    led.print(i)
    time.sleep(1)
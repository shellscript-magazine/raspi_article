import time
import lirc
import RPi.GPIO as GPIO

LED1 = 14
LED2 = 15
LED3 = 12
LED4 = 16

leds = [LED1, LED2, LED3 ,LED4]
flag_a = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

socketid = lirc.init('rctest', './rctest.lircrc')

while True:
        code = lirc.nextcode()
        if code[0] == 'button_a':
                flag_a ^=  1
                GPIO.output(LED1, flag_a)
        elif code[0] == 'button_b':
                break
GPIO.cleanup()

import RPi.GPIO as GPIO
import time

P_A = 21
P_B = 25

class rotaryenc():

    def __init__(self, phase_a = P_A, phase_b = P_B):
        self.phase_a = phase_a
        self.phase_b = phase_b

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(phase_a, GPIO.IN)
        GPIO.setup(phase_b, GPIO.IN)

        GPIO.add_event_detect(phase_a,  GPIO.RISING, callback=self.__changeStatus)

        self.__callback = None
        self.prev_forward_time = 0
        self.prev_backward_time = 0

    def __changeStatus(self, gpio):
        pa = GPIO.input(self.phase_a)
        pb = GPIO.input(self.phase_b)
        if pa == GPIO.LOW:     # チャタリング等
            return
        
        value = 0
        current = time.time()
        if pb == GPIO.LOW: # 時計回り
            value = 1
            if self.prev_forward_time != 0:
                if (current - self.prev_forward_time) < 0.1:    # 100ms以内
                    value = 10
            self.prev_forward_time = current
            self.prev_backward_time = 0
        if pb == GPIO.HIGH:
            value = -1
            if self.prev_backward_time != 0:
                if (current - self.prev_backward_time) < 0.1:    # 100ms以内
                    value = -10
            self.prev_forward_time = 0
            self.prev_backward_time = current

        if value != 0 and self.__callback is not None:
            self.__callback(value)
    
    def registerCallback(self, c):
        self.__callback = c
        return
    
    def unregisterCallback(self):
        self.__callback = None

    def __del__(self):
        GPIO.cleanup()

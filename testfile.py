from gpiozero import Button
from gpiozero.pins.pigpio import PiGPIOFactory
import time

IP_ADRESS = PiGPIOFactory('192.168.1.29')
button = Button(pin=22, pin_factory=IP_ADRESS)
print("Program Initiated")


def check_press_time(b):
    if b.value == 1:
        start = time.time()
        b.wait_for_inactive()
        if b.value == 0:
            end = time.time()
            press_time = end - start
            print("press_time = ")
            print(press_time)
            print('\n')

while True:
    check_press_time(button)

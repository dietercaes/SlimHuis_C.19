#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "1.0"

# IMPORTS
from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button
import time

# CONSTANTS
IP_ADRESS = PiGPIOFactory('192.168.1.29')
RELAY_PINS = [13, 26, 6, 5]
BUTTON_PINS = [22, 27, 17, 4]
BUTTON_DELAY = 0.4
LONG_PRESS_TIME = 0.5
NUMBER_OF_BUTTONS = len(BUTTON_PINS)
ON_TIME_LONG_PRESS = 3
BLINK_TIME_LONG_PRESS = 25
BLINK_DELAY = 1

# VARIABLES
relays = []
buttons = []


# FUNCTIONS
def create_relays():
    for i in RELAY_PINS:
        relays.append(DigitalOutputDevice(pin=i, pin_factory=IP_ADRESS))


def create_buttons():
    for i in BUTTON_PINS:
        buttons.append(Button(pin=i, bounce_time=0.3, hold_time=0.5, pin_factory=IP_ADRESS))


def check_buttons():
    while True:
        for i in range(NUMBER_OF_BUTTONS):
            check_for_press(i)


def check_for_press(index):
    if check_status(index) == 1:
        check_long_press(index)
        relays[index].on()

    if check_status(index) == 0:
        check_long_press(index)
        relays[index].off()


def check_status(index):
    if buttons[index].value == 1 and relays[index].value == 0:
        return True
    if buttons[index].value == 1 and relays[index].value == 1:
        return False


def check_long_press(index):
    if buttons[index].held_time is not None:
        if buttons[index].held_time >= LONG_PRESS_TIME:
            long_press(index)


def long_press(index):
    relays[index].on()
    time.sleep(ON_TIME_LONG_PRESS)
    blink(index, BLINK_TIME_LONG_PRESS)


def blink(index, duration):
    t = 0
    while t < duration:
        if relays[index].value == 0:
            relays[index].on()
            time.sleep(BLINK_DELAY)
            t = t + 1

        if relays[index].value == 1:
            relays[index].off()
            time.sleep(BLINK_DELAY)
            t = t + 1


# MAIN
def main():
    print("Program started.")
    create_relays()
    create_buttons()
    check_buttons()


if __name__ == '__main__':
    main()

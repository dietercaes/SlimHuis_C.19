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
NUMBER_OF_BUTTONS = len(BUTTON_PINS)

# VARIABLES
relays = []
buttons = []


# FUNCTIONS
def create_relays():
    for i in RELAY_PINS:
        relays.append(DigitalOutputDevice(pin=i, pin_factory=IP_ADRESS))


def create_buttons():
    for i in BUTTON_PINS:
        buttons.append(Button(pin=i, pin_factory=IP_ADRESS))


def check_button():
    while True:
        for i in range(NUMBER_OF_BUTTONS):
            check_for_press(i)


def check_for_press(index):
    if check_status(index) == 1:
        relays[index].on()
        time.sleep(BUTTON_DELAY)

    if check_status(index) == 0:
        relays[index].off()
        time.sleep(BUTTON_DELAY)


def check_status(index):
    if buttons[index].value == 1 and relays[index].value == 0:
        return True
    if buttons[index].value == 1 and relays[index].value == 1:
        return False


# MAIN
def main():
    print("Program started.")
    create_relays()
    create_buttons()
    check_button()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "1.0"

# IMPORTS
from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button
import time

# VARIABLES
IP_ADRESS = PiGPIOFactory('192.168.1.29')       # Change IP adress to the IP adress of your raspberry pi.
RELAY_PINS = [13, 26, 6, 5]                     # The GPIO output pins connected to the relays.
number_of_relays = len(RELAY_PINS)
relays = []                                     # List to store
BUTTON_PINS = [22, 27, 17, 4]                   # The GPIO input pins connected to the pushbuttons.
number_of_buttons = len(BUTTON_PINS)
buttons = []
BUTTON_DELAY_TIME = 0.4


def create_relays():
    for i in RELAY_PINS:
        relays.append(DigitalOutputDevice(pin=i, pin_factory=IP_ADRESS))


def create_buttons():
    for i in BUTTON_PINS:
        buttons.append(Button(pin=i, pin_factory=IP_ADRESS))


def check_button():
    while True:
        for i in range(number_of_buttons):
            check_for_press(i)


def check_for_press(index):
    if buttons[index].value == 1 and relays[index].value == 0:
        relays[index].on()
        time.sleep(BUTTON_DELAY_TIME)

    if buttons[index].value == 1 and relays[index].value == 1:
        relays[index].off()
        time.sleep(BUTTON_DELAY_TIME)


# MAIN
def main():
    create_relays()
    create_buttons()
    check_button()


if __name__ == '__main__':
    main()

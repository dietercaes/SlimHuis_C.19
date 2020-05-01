#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "2.0"

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
LONG_PRESS_TIME = 1
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
        buttons.append(Button(pin=i, pin_factory=IP_ADRESS))


def check_buttons():
    while True:
        for i in range(NUMBER_OF_BUTTONS):
            check_for_press(i)


def check_for_press(index):
    state = check_relay_state(index)
    if state[0] == 1:                       # Checking current relay state.
        if state[1] > LONG_PRESS_TIME:      # Checking for long press.
            execute_long_press(index, 1)
        relays[index].on()
        time.sleep(BUTTON_DELAY)

    if state[0] == 0:
        relays[index].off()
        time.sleep(BUTTON_DELAY)


def check_relay_state(index):
    if buttons[index].value == 1:               # Check button is currently being pressed.
        start_time = time.time()                # Starting the timer to check time pressed.
        press_type = is_long_press(start_time)
        if relays[index].value == 0:
            return False, press_type
    if buttons[index].value == 1:
        press_type = is_long_press()
        if relays[index].value == 1:
            return True, press_type


def calculate_time(start):
    end = time.time()
    time_value = end - start
    return time_value


def check_press_time(index):
    if index.value == 1:
        start = time.time()
        index.wait_for_inactive()
        if index.value == 0:
            end = time.time()
            press_time = end - start
            print("press_time = ")
            print(press_time)
            print('\n')
            return press_time


def is_long_press(start_time):
    if calculate_time(start_time) >= LONG_PRESS_TIME:
        return True
    if calculate_time(start_time) < LONG_PRESS_TIME:
        return False


def execute_long_press(index, current_relay_state):
    if current_relay_state == 0:
        relays[index].on()
        time.sleep(ON_TIME_LONG_PRESS)
        blink(index, BLINK_TIME_LONG_PRESS)
    if current_relay_state == 1:                # light on for 10 sec then turns off
        relays[index].on()
        time.sleep(10)
        relays[index].off()


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

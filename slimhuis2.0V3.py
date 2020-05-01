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
NUMBER_OF_RELAYS = len(RELAY_PINS)
ON_TIME_LONG_PRESS = 30
BLINK_TIME_LONG_PRESS = 25
BLINK_DELAY = 1
DOUBLE_CLICK_TIME = 0.4

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
    press_type = check_press_type(index)
    state = check_state(index)
    if press_type is not None:
        if press_type == "long press" and state is False:  # long, single press
            execute_long_press(index, current_relay_state=0)
        if press_type == "long press" and state is True:
            execute_long_press(index, current_relay_state=1)

        if press_type == 200 and state is False:  # Double press
            execute_double_press(current_relay_state=0)
        if press_type == 200 and state is True:
            execute_double_press(current_relay_state=1)

        if press_type == 300 and state is False:  # Triple press
            execute_triple_press(index, current_relay_state=0)
        if press_type == 300 and state is True:
            execute_triple_press(index, current_relay_state=1)

        elif press_type == "single press" and state is False:  # short, single press
            relays[index].on()
        elif press_type == "single press" and state is True:
            relays[index].off()


def check_state(index):
    if relays[index].value == 0:
        return False
    if relays[index].value == 1:
        return True


def check_press_type(index):
    press_time = calculate_press_time(index)
    if press_time is not None:
        if press_time >= LONG_PRESS_TIME:
            return "long press"
        buttons[index].wait_for_active(timeout=DOUBLE_CLICK_TIME)

        second_press_time = calculate_press_time(index)
        if second_press_time is not None:
            if second_press_time < DOUBLE_CLICK_TIME:
                buttons[index].wait_for_active(timeout=DOUBLE_CLICK_TIME)

                third_press_time = calculate_press_time(index)
                if third_press_time is not None:
                    if third_press_time < DOUBLE_CLICK_TIME:
                        return 300
                else:
                    return 200
        else:
            return "single press"


def calculate_press_time(index):
    if buttons[index].value == 1:  # Button pushed down
        start = time.time()
        buttons[index].wait_for_inactive()  # Wait on button release
        if buttons[index].value == 0:
            end = time.time()
            press_time = end - start  # First press time
            return press_time


def execute_long_press(index, current_relay_state):
    if current_relay_state == 0:
        relays[index].on()
        time.sleep(ON_TIME_LONG_PRESS)
        blink(index, BLINK_TIME_LONG_PRESS)
    if current_relay_state == 1:  # light on for 10 sec then turns off
        relays[index].on()
        time.sleep(10)
        relays[index].off()


def execute_double_press(current_relay_state):
    if current_relay_state == 0:
        for i in range(NUMBER_OF_RELAYS):
            relays[i].on()
    if current_relay_state == 1:
        for i in range(NUMBER_OF_RELAYS):
            relays[i].off()
        # active_relays = []
        # for i in range(NUMBER_OF_RELAYS):
        #     if relays[i].value == 1:
        #         active_relays.append(i)
        #         number_of_active_relays = len(active_relays)
        #         for j in range(number_of_active_relays):
        #             relays[j].off()


def execute_triple_press(index, current_relay_state):
    if current_relay_state == 0:
        for i in range(NUMBER_OF_RELAYS):
            relays[i].on()
        time.sleep(30)
        blink_all(25)
    if current_relay_state == 1:
        time.sleep(10)
        for i in range(NUMBER_OF_RELAYS):
            relays[i].off()


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


def blink_all(duration):
    counter = 0
    while counter < duration:
        # execute_double_press(0)
        # time.sleep(BLINK_DELAY)
        # execute_double_press(1)
        value = counter % 2
        execute_double_press(value)
        time.sleep(BLINK_DELAY)
        counter = counter + 1


# MAIN
def main():
    print("Program started.")
    create_relays()
    create_buttons()
    check_buttons()


if __name__ == '__main__':
    main()

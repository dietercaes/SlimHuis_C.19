#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "2.3"

# IMPORTS
from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button
import time
import multiprocessing

# CONSTANTS
IP_ADRESS = PiGPIOFactory('192.168.1.29')  # Change IP adress to the IP adress of your raspberry pi.
RELAY_PINS = [13, 26, 6, 5]  # The GPIO output pins connected to the relays.
BUTTON_PINS = [22, 27, 17, 4]  # The GPIO output pins connected to the relays.
BUTTON_DELAY = 0.4  # Button debounce delay.
LONG_PRESS_TIME = 1.5
NUMBER_OF_BUTTONS = len(BUTTON_PINS)
NUMBER_OF_RELAYS = len(RELAY_PINS)
ON_TIME_LONG_PRESS = 30
BLINK_TIME_LONG_PRESS = 25
BLINK_DELAY = 1
DOUBLE_CLICK_TIME = 0.5  # Time window to press button another time.

# VARIABLES
relays = []  # Lists to store DigitalOutputDevice and Button objects.
buttons = []
processes = []


# FUNCTIONS
def create_relays():  # Initialising relays as DigitalOutputDevice objects.
    for i in RELAY_PINS:
        relays.append(DigitalOutputDevice(pin=i, pin_factory=IP_ADRESS))


def create_buttons():  # Initialising buttons as Button objects.
    for i in BUTTON_PINS:
        buttons.append(Button(pin=i, pin_factory=IP_ADRESS))


# def check_buttons():
#     while True:
#         for i in range(NUMBER_OF_BUTTONS):
#             check_for_press(i)


def check_button(index, relay_list, button_list):
    while True:
        check_for_press(index, relay_list, button_list)


def check_for_press(index, relay_list, button_list):  # Executing different actions depending on press type and
    # current relay state.
    press_type = check_press_type(index, relay_list, button_list)
    state = check_state(index, relay_list)
    if press_type is not None:
        if press_type == "long press" and state is False:  # Long press
            execute_long_press(index, relay_list=relay_list, current_relay_state=0)
        if press_type == "long press" and state is True:
            execute_long_press(index, relay_list=relay_list, current_relay_state=1)

        if press_type == "double" and state is False:  # Double press
            execute_double_press(current_relay_state=0, relay_list=relay_list)
        if press_type == "double" and state is True:
            execute_double_press(current_relay_state=1, relay_list=relay_list)

        if press_type == "triple" and state is False:  # Triple press
            execute_triple_press(current_relay_state=0, relay_list=relay_list)
        if press_type == "triple" and state is True:
            execute_triple_press(current_relay_state=1, relay_list=relay_list)

        elif press_type == "single press" and state is False:  # short, single press
            relay_list[index].on()  # Light goes on as normal.
        elif press_type == "single press" and state is True:
            relay_list[index].off()  # Light goes off as normal.


def check_state(index, relay_list):  # Check whether the switch is currently on or off.
    if relay_list[index].value == 0:
        return False
    if relay_list[index].value == 1:
        return True


def check_press_type(index, relay_list,
                     button_list):  # Differentiating between short press, long press, double and triple press.
    press_time = calculate_press_time(index, relay_list)
    if press_time is not None:
        if press_time >= LONG_PRESS_TIME:
            return "long press"
        button_list[index].wait_for_active(timeout=DOUBLE_CLICK_TIME)

        second_press_time = calculate_press_time(index, relay_list)
        if second_press_time is not None:
            if second_press_time < DOUBLE_CLICK_TIME:
                button_list[index].wait_for_active(timeout=DOUBLE_CLICK_TIME)

                third_press_time = calculate_press_time(index, relay_list)
                if third_press_time is not None:
                    if third_press_time < DOUBLE_CLICK_TIME:
                        return "triple"
                else:
                    return "double"
        else:
            return "single press"


def calculate_press_time(index, button_list):
    if button_list[index].value == 1:  # Button pushed down.
        start = time.time()
        button_list[index].wait_for_inactive()  # Wait on button release.
        if button_list[index].value == 0:
            end = time.time()
            press_time = end - start  # Press time.
            return press_time


def execute_long_press(index, relay_list, current_relay_state):
    if current_relay_state == 0:  # Light is 30sec on, after 25sec it starts blinking.
        relay_list[index].on()
        time.sleep(ON_TIME_LONG_PRESS)
        blink(index, relay_list, BLINK_TIME_LONG_PRESS)
    if current_relay_state == 1:  # Light stays on for 10 more sec then turns off.
        relay_list[index].on()
        time.sleep(10)
        relay_list[index].off()


def execute_double_press(current_relay_state, relay_list):
    if current_relay_state == 0:  # All lights go on.
        for i in range(NUMBER_OF_RELAYS):
            relay_list[i].on()
    if current_relay_state == 1:  # All lights that are on that moment go off.
        for i in range(NUMBER_OF_RELAYS):
            relay_list[i].off()


def execute_triple_press(current_relay_state, relay_list):
    if current_relay_state == 0:  # All light 30sec on, after 25sec it starts blinking.
        for i in range(NUMBER_OF_RELAYS):
            relay_list[i].on()
        time.sleep(30)
        blink_all(25, relay_list)
    if current_relay_state == 1:  # All lights that are on that moment go off after 10 secs.
        time.sleep(10)
        for i in range(NUMBER_OF_RELAYS):
            relay_list[i].off()


def blink(index, relay_list, duration):
    t = 0
    while t < duration:
        if relay_list[index].value == 0:
            relay_list[index].on()
            time.sleep(BLINK_DELAY)
            t = t + 1

        if relay_list[index].value == 1:
            relay_list[index].off()
            time.sleep(BLINK_DELAY)
            t = t + 1


def blink_all(duration, relay_list):
    counter = 0
    while counter < duration:
        value = counter % 2
        execute_double_press(value, relay_list)
        time.sleep(BLINK_DELAY)
        counter = counter + 1


# MAIN
def main():
    print("Program started.")
    create_relays()
    create_buttons()

    for i in range(NUMBER_OF_BUTTONS):
        p = multiprocessing.Process(target=check_button, args=[i, relays, buttons])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "3.4"

# IMPORTS
from gpiozero import DigitalOutputDevice
from gpiozero import Button
from gpiozero.pins.pigpio import PiGPIOFactory
import multiprocessing
import time
from multiprocessing import Manager

# CONSTANTS
IP_ADRESS = PiGPIOFactory('192.168.1.29')  # Change IP adress to the IP adress of your raspberry pi.
RELAY_PINS = [13, 26, 6, 5]  # The GPIO output pins connected to the relays.
BUTTON_PINS = [22, 27, 17, 4]  # The GPIO output pins connected to the relays.
BUTTON_DELAY = 0.4
LONG_PRESS_TIME = 1.5
NUMBER_OF_BUTTONS = len(BUTTON_PINS)
NUMBER_OF_RELAYS = len(RELAY_PINS)
ON_TIME_LONG_PRESS = 25
BLINK_TIME_LONG_PRESS = 5
BLINK_DELAY = 1
DOUBLE_CLICK_TIME = 0.5

# VARIABLES
relays = []  # Lists to store DigitalOutputDevice and Button objects.
buttons = []
relay_name_list = []
button_name_list = []
processes = []
dictionary = {}

for i in range(NUMBER_OF_RELAYS):
    relay_name_list.append("relay" + str(i + 1))
for i in range(NUMBER_OF_BUTTONS):
    button_name_list.append("button" + str(i + 1))
for i in RELAY_PINS:
    relays.append(DigitalOutputDevice(pin=i, pin_factory=IP_ADRESS))
for i in BUTTON_PINS:
    buttons.append(Button(pin=i, pin_factory=IP_ADRESS))
relay_name_list.extend(button_name_list)
relay_and_button_keys = relay_name_list
relays.extend(buttons)
relay_and_button_values = relays
dictionary = dict(zip(relay_and_button_keys, relay_and_button_values))


# MAIN
def main():
    print("Program started.")
    for i in range(NUMBER_OF_BUTTONS):
        p = multiprocessing.Process(target=check_button, args=[i])
        p.start()
        processes.append(p)
    for process in processes:
        process.join()


# FUNCTIONS
def create_relay_keys():
    for i in range(NUMBER_OF_RELAYS):
        relay_name_list.append("relay" + str(i + 1))


def create_button_keys():
    for i in range(NUMBER_OF_BUTTONS):
        button_name_list.append("button" + str(i + 1))


def create_relays():  # Initialising relays as DigitalOutputDevice objects.
    for i in RELAY_PINS:
        relays.append(DigitalOutputDevice(pin=i, pin_factory=IP_ADRESS))


def create_buttons():  # Initialising buttons as Button objects.
    for i in BUTTON_PINS:
        buttons.append(Button(pin=i, pin_factory=IP_ADRESS))


def create_dictionary():
    relay_name_list.extend(button_name_list)
    relay_and_button_keys = relay_name_list
    relays.extend(buttons)
    relay_and_button_values = relays
    d = dict(zip(relay_and_button_keys, relay_and_button_values))
    return d


def check_button(index):
    while True:
        check_for_press(index)


def check_for_press(index):
    d = dict(dictionary)
    press_type = check_press_type(index, d)
    state = check_state(index, d)
    if press_type is not None:
        if press_type == "long press" and state is False:  # long, single press
            execute_long_press(index, current_relay_state=0, d=d)
        if press_type == "long press" and state is True:
            execute_long_press(index, current_relay_state=1, d=d)

        if press_type == 2 and state is False:  # Double press
            execute_double_press(current_relay_state=0, d=d)
        if press_type == 2 and state is True:
            execute_double_press(current_relay_state=1, d=d)

        if press_type == 3 and state is False:  # Triple press
            execute_triple_press(current_relay_state=0, d=d)
        if press_type == 3 and state is True:
            execute_triple_press(current_relay_state=1, d=d)

        elif press_type == "single press" and state is False:  # short, single press
            d["relay" + str(index + 1)].on()
        elif press_type == "single press" and state is True:
            d["relay" + str(index + 1)].off()


def check_state(index, d):
    if d["relay" + str(index + 1)].value == 0:
        return False
    if d["relay" + str(index + 1)].value == 1:
        return True


def check_press_type(index, d):  # Differentiating between short press, long press, double and triple press.
    press_time = calculate_press_time(index, d)
    if press_time is not None:
        if press_time >= LONG_PRESS_TIME:
            return "long press"
        d["button" + str(index + 1)].wait_for_active(timeout=DOUBLE_CLICK_TIME)

        second_press_time = calculate_press_time(index, d)
        if second_press_time is not None:
            if second_press_time < DOUBLE_CLICK_TIME:
                d["button" + str(index + 1)].wait_for_active(timeout=DOUBLE_CLICK_TIME)

                third_press_time = calculate_press_time(index, d)
                if third_press_time is not None:
                    if third_press_time < DOUBLE_CLICK_TIME:
                        return 3
                else:
                    return 2
        else:
            return "single press"


def calculate_press_time(index, d):
    if d["button" + str(index + 1)].value == 1:  # Button pushed down.
        start = time.time()
        d["button" + str(index + 1)].wait_for_inactive()  # Wait on button release.
        if d["button" + str(index + 1)].value == 0:
            end = time.time()
            press_time = end - start  # Press time.
            return press_time


def execute_long_press(index, current_relay_state, d):
    if current_relay_state == 0:
        d["relay" + str(index + 1)].on()
        time.sleep(ON_TIME_LONG_PRESS)
        blink(index, BLINK_TIME_LONG_PRESS, d)
    if current_relay_state == 1:  # light on for 10 sec then turns off
        d["relay" + str(index + 1)].on()
        time.sleep(10)
        d["relay" + str(index + 1)].off()


def execute_double_press(current_relay_state, d):
    if current_relay_state == 0:
        for i in range(NUMBER_OF_RELAYS):
            d["relay" + str(i + 1)].on()
    if current_relay_state == 1:
        for i in range(NUMBER_OF_RELAYS):
            d["relay" + str(i + 1)].off()
        # active_relays = []
        # for i in range(NUMBER_OF_RELAYS):
        #     if relays[i].value == 1:
        #         active_relays.append(i)
        #         number_of_active_relays = len(active_relays)
        #         for j in range(number_of_active_relays):
        #             relays[j].off()


def execute_triple_press(current_relay_state, d):
    if current_relay_state == 0:
        for i in range(NUMBER_OF_RELAYS):
            d["relay" + str(i + 1)].on()
        time.sleep(30)
        blink_all(25, d)
    if current_relay_state == 1:
        time.sleep(10)
        for i in range(NUMBER_OF_RELAYS):
            d["relay" + str(i + 1)].off()


def blink(index, duration, d):
    t = 0
    while t < duration:
        if d["relay" + str(index + 1)].value == 0:
            d["relay" + str(index + 1)].on()
            time.sleep(BLINK_DELAY)
            t = t + 1

        if d["relay" + str(index + 1)].value == 1:
            d["relay" + str(index + 1)].off()
            time.sleep(BLINK_DELAY)
            t = t + 1


def blink_all(duration, d):
    counter = 0
    while counter < duration:
        value = counter % 2
        execute_double_press(value, d)
        time.sleep(BLINK_DELAY)
        counter = counter + 1


if __name__ == '__main__':
    main()

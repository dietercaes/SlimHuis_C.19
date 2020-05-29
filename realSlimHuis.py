#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "3.5"

# IMPORTS
import gpiozero
from gpiozero import DigitalOutputDevice
from gpiozero import Button
import time

# CONSTANTS
RELAY_PINS = [13, 26]  # The GPIO output pins connected to the relays.
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
io_devices = {}


# MAIN
def main():
    print("Smart Home Started")
    create_relay_keys()
    create_button_keys()
    create_relays()
    create_buttons()
    check_buttons()


# FUNCTIONS
def create_relay_keys():
    print("Creating relay keys ...")
    for i in range(NUMBER_OF_RELAYS):
        relay_name_list.append("relay" + str(i + 1))


def create_button_keys():
    print("Creating button keys ...")
    for i in range(NUMBER_OF_BUTTONS):
        button_name_list.append("button" + str(i + 1))


def create_relays():  # Initialising relays as DigitalOutputDevice objects.
    print("Creating relay objects ...")
    for i in RELAY_PINS:
        relays.append(DigitalOutputDevice(pin=i))


def create_buttons():  # Initialising buttons as Button objects.
    print("Creating button objects ...")
    for i in BUTTON_PINS:
        buttons.append(Button(pin=i))


def create_dictionary():
    print("Creating dictionary ...")
    relay_name_list.extend(button_name_list)
    relay_and_button_keys = relay_name_list

    relays.extend(buttons)
    relay_and_button_values = relays

    dictionary = dict(zip(relay_and_button_keys, relay_and_button_values))
    return dictionary


def check_buttons():
    print("Loop started, checking for button press ...")
    dictionary = create_dictionary()
    while True:
        for i in range(NUMBER_OF_BUTTONS):
            check_for_press(i, dictionary)


def check_for_press(index, d):
    press_type = check_press_type(index, d)
    i = check_corresponding_relay(index)
    state = check_state(i, d)
    if press_type is not None:
        if press_type == "long press" and state is False:  # long, single press
            execute_long_press(i, current_relay_state=0, d=d)
        if press_type == "long press" and state is True:
            execute_long_press(i, current_relay_state=1, d=d)

        if press_type == 2 and state is False:  # Double press
            execute_double_press(current_relay_state=0, d=d)
        if press_type == 2 and state is True:
            execute_double_press(current_relay_state=1, d=d)

        if press_type == 3 and state is False:  # Triple press
            execute_triple_press(current_relay_state=0, d=d)
        if press_type == 3 and state is True:
            execute_triple_press(current_relay_state=1, d=d)

        elif press_type == "single press" and state is False:  # short, single press
            d["relay" + str(i + 1)].on()
        elif press_type == "single press" and state is True:
            d["relay" + str(i + 1)].off()


def check_state(index, d):
    if d["relay" + str(index + 1)].value == 0:
        return False
    if d["relay" + str(index + 1)].value == 1:
        return True


def check_corresponding_relay(index):
    if index % 2 == 0:
        return 1
    if index + 2 == 1:
        return 2


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

from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button
import time

IP_ADRESS = PiGPIOFactory('192.168.1.29')

RELAY_1 = DigitalOutputDevice(pin=13, pin_factory=IP_ADRESS)
RELAY_2 = DigitalOutputDevice(pin=26, pin_factory=IP_ADRESS)
RELAY_3 = DigitalOutputDevice(pin=6, pin_factory=IP_ADRESS)
RELAY_4 = DigitalOutputDevice(pin=5, pin_factory=IP_ADRESS)

RELAY_PINS = [13, 26, 6, 5]
RELAYS = []
number_of_relays = len(RELAY_PINS)

for i in RELAY_PINS:
    a = DigitalOutputDevice(pin=13, pin_factory=IP_ADRESS)

print(RELAYS)

















BUTTON_1 = Button(pin=22, pin_factory=IP_ADRESS)
BUTTON_2 = Button(pin=27, pin_factory=IP_ADRESS)
BUTTON_3 = Button(pin=17, pin_factory=IP_ADRESS)
BUTTON_4 = Button(pin=4, pin_factory=IP_ADRESS)

#BUTTON_PINS = [22, 27, 17, 4]
#number_of_buttons = len(BUTTONS)


#def create_relays(relay_list):
#    for i in relay_list:
#        RELAY[i] = DigitalOutputDevice(pin = i, pin_factory=IP_ADRESS)


#def create_buttons(button_list):
#    for i in button_list:
#        BUTTONS[i] = Button(pin = i, pin_factory=IP_ADRESS)


def main():
    #create_relays(RELAYS)
    #create_buttons(BUTTONS)
    while True:
        if BUTTON_1.value == 1 and RELAY_1.value == 0:
            RELAY_1.on()
            time.sleep(0.25)
        if BUTTON_1.value == 1 and RELAY_1.value == 1:
            RELAY_1.off()
            time.sleep(0.25)

        if BUTTON_2.value == 1 and RELAY_2.value == 0:
            RELAY_2.on()
            time.sleep(0.25)
        if BUTTON_2.value == 1 and RELAY_2.value == 1:
            RELAY_2.off()
            time.sleep(0.25)

        if BUTTON_3.value == 1 and RELAY_3.value == 0:
            RELAY_3.on()
            time.sleep(0.25)
        if BUTTON_3.value == 1 and RELAY_3.value == 1:
            RELAY_3.off()
            time.sleep(0.25)

        if BUTTON_4.value == 1 and RELAY_4.value == 0:
            RELAY_4.on()
            time.sleep(0.25)
        if BUTTON_4.value == 1 and RELAY_4.value == 1:
            RELAY_4.off()
            time.sleep(0.25)


if __name__ == '__main__':
    main()

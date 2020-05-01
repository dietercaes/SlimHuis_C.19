#!/usr/bin/env python
__author__ = "Dieter Caes"
__version__ = "1.0"

import random

master_number = [random.random()*9999]
attempts = 0


def main():
    print("Welcome to mastermind!\n")
    print("Enter a number:\n")
    user_number = input()
    if user_number == master_number:
        print("Congratulations you won in " + attempts)

    if user_number != master_number:
        answer = False


if __name__ == '__main__':
    main()
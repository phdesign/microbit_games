from microbit import *
from time import sleep
from random import randint
import math

class Input:
    BUTTON_A = 1
    BUTTON_B = 2

OPTIONS = [
    (Image.ARROW_W, Input.BUTTON_A),
    (Image.ARROW_E, Input.BUTTON_B)
]
WAIT_START = 1500
DECAY_RATE = 200

def create_exponential_decay(inital_value, decay_rate):
    def exponential_decay(time):
        return inital_value * math.exp(-(1 / decay_rate) * time)
    return exponential_decay


def wait_for_input(wait_for):
    start = running_time()
    while True:
        if button_a.is_pressed():
            return Input.BUTTON_A
        elif button_b.is_pressed():
            return Input.BUTTON_B

        elapsed = running_time() - start
        if elapsed > wait_for:
            return None

def play():
    score = 0

    display.show("3")
    sleep(700)
    display.show("2")
    sleep(700)
    display.show("1")
    sleep(1000)

    start = running_time()
    wait_decay = create_exponential_decay(WAIT_START, DECAY_RATE);
    while True:
        elapsed = running_time() - start
        wait = round(wait_decay(elapsed / 1000))
        option, expected = OPTIONS[randint(0, 1)]
        display.show(option)
        result = wait_for_input(wait)
        if result == expected:
            score += 1
            sleep(1000)
        else:
            display.show(Image.NO)
            sleep(1000)
            break
    
    display.scroll("Score: {:d}".format(score))

if __name__ == "__main__":
    while True:
        if button_a.is_pressed():
            play()
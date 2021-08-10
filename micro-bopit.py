from microbit import *
from random import randint

class Input:
    BUTTON_A = 1
    BUTTON_B = 2

OPTIONS = [
    (Image.ARROW_W, Input.BUTTON_A),
    (Image.ARROW_E, Input.BUTTON_B)
]
WAIT = 1500

def wait_for_input():
    start = running_time()
    while True:
        if button_a.is_pressed():
            return Input.BUTTON_A
        elif button_b.is_pressed():
            return Input.BUTTON_B

        elapsed = running_time() - start
        if elapsed > WAIT:
            return None

def play():
    score = 0

    display.show("3")
    sleep(700)
    display.show("2")
    sleep(700)
    display.show("1")
    sleep(1000)
    while True:
        option, expected = OPTIONS[randint(0, 1)]
        display.show(option)
        result = wait_for_input()
        if result == expected:
            display.show(Image.HAPPY)
            score += 1
            sleep(1000)
        else:
            display.show(Image.SAD)
            sleep(1000)
            break
    
    display.scroll("Score: {:d}".format(score))

while True:
    if button_a.is_pressed():
        play()
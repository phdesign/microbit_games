from microbit import *
from time import sleep
from random import randint
import math
import music

class Input:
    BUTTON_A = 1
    BUTTON_B = 2
    PIN_LOGO = 3

class Option:
    def __init__(self, prompt, exected, sound):
        self.prompt = prompt
        self.expected = exected
        self.sound = sound

OPTIONS = [
    Option(Image.ARROW_W, Input.BUTTON_A, "D4:4"),
    Option(Image.ARROW_E, Input.BUTTON_B, "E4:4"),
    Option(Image.ARROW_N, Input.PIN_LOGO, "F4:4")
]
WAIT_START_MS = 1500
DECAY_RATE = 50
VOLUME = 160

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
        elif pin_logo.is_touched():
            return Input.PIN_LOGO

        elapsed = running_time() - start
        if elapsed > wait_for:
            return None

def play():
    score = 0

    display.clear()
    music.play(music.JUMP_UP, wait=False)
    display.show("3")
    sleep(0.7)
    display.show("2")
    sleep(0.7)
    display.show("1")
    sleep(1)

    start = running_time()
    wait_decay = create_exponential_decay(WAIT_START_MS, DECAY_RATE);
    while True:
        elapsed_sec = (running_time() - start) / 1000
        wait_ms = round(wait_decay(elapsed_sec), 4)

        option = OPTIONS[randint(0, 2)]
        display.show(option.prompt)
        music.play(option.sound)

        result = wait_for_input(wait_ms)
        if result == option.expected:
            score += 1
            display.clear()
            sleep(round(wait_ms / 2000, 4))
        else:
            music.play(music.POWER_DOWN, wait=False)
            display.show(Image.NO)
            sleep(1)
            break
    
    return score

if __name__ == "__main__":
    set_volume(VOLUME)
    high_score = 0
    while True:
        if button_a.is_pressed():
            score = play()
            if score > high_score:
                high_score = score
                music.play(music.PRELUDE, wait=False)
                display.show(Image.HAPPY)
                sleep(1)
                display.scroll("High score: {:d}".format(score), wait=False)
            else:
                display.scroll("Score: {:d}".format(score), wait=False)

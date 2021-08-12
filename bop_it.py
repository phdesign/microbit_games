from microbit import *
from time import sleep
from random import randint
import math

import music

# The starting time in milliseconds we will wait for a response.
WAIT_START_MS = 1500
# How quickly the wait time reduces. A smaller value means it shortens more quickly.
DECAY_RATE = 50
# Starting sound volume
START_VOLUME = 160
# Maximum volume
MAX_VOLUME = 255
# Number of steps that the volume will change in
VOLUME_STEPS = 5
# Volume indicator image to show
VOLUME_IMAGE = Image("55555:66666:77777:88888:99999")
# Repeat press the button within this time to change the volume, rather than just show it
VOLUME_CHANGE_WAIT = 3000


class Input:
    BUTTON_A = 1
    BUTTON_B = 2
    PIN_LOGO = 3


class Option:
    def __init__(self, prompt, exected, sound):
        self.prompt = prompt
        self.expected = exected
        self.sound = sound


def volume_to_step(volume):
    """Converts an absolute volume (0-255) to a relative step (0-5)."""
    return round((volume / MAX_VOLUME) * VOLUME_STEPS)


def show_volume(step):
    """Displays the current volume."""
    image = VOLUME_IMAGE.shift_down(VOLUME_STEPS - step)
    display.show(image, delay=500, clear=True)


def change_volume(volume):
    """Cycles incrementing the volume, resetting to zero after max."""
    step = volume_to_step(volume)
    new_step = step + 1 if step < VOLUME_STEPS else 0
    new_volume = math.floor((MAX_VOLUME / VOLUME_STEPS) * new_step)
    set_volume(new_volume)
    music.play("A5:2", wait=False)
    show_volume(new_step)
    return new_volume


def create_exponential_decay(inital_value, decay_rate):
    """Creates an exponential decay function.

    Given an initial value (wait time) and decay rate, returns
    a function that exponentially decays over time.
    A smaller decay rate means it decays over a shortened period.
    """

    def exponential_decay(time):
        return inital_value * math.exp(-(1 / decay_rate) * time)

    return exponential_decay


def wait_for_input(wait_for):
    """Waits for an input for a set time.

    Returns the input or None if it timed out.
    """
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


def play(options):
    """Play one round of the game."""
    score = 0

    # Show a starting animation
    display.clear()
    music.play(music.JUMP_UP, wait=False)
    display.show("3")
    sleep(0.7)
    display.show("2")
    sleep(0.7)
    display.show("1")
    sleep(1)

    start = running_time()
    wait_decay = create_exponential_decay(WAIT_START_MS, DECAY_RATE)
    while True:
        elapsed_sec = (running_time() - start) / 1000
        wait_ms = round(wait_decay(elapsed_sec), 4)

        # Pick a random input option
        option = options[randint(0, 2)]
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


def main():
    """Main game loop."""

    volume = START_VOLUME
    options = [
        Option(Image.ARROW_W, Input.BUTTON_A, "D4:4"),
        Option(Image.ARROW_E, Input.BUTTON_B, "E4:4"),
        Option(Image.ARROW_N, Input.PIN_LOGO, "F4:4"),
    ]
    high_score = 0
    set_volume(volume)
    button_b_last_pushed = 0

    while True:
        # Press A to start the game
        if button_a.is_pressed():
            score = play(options)
            # Check if this was a high score
            if score > high_score:
                high_score = score
                music.play(music.PRELUDE, wait=False)
                display.show(Image.HAPPY)
                sleep(1)
                display.scroll("High score: {:d}".format(score), wait=False)
            else:
                display.scroll("Score: {:d}".format(score), wait=False)

        # Press B to show or change volume
        if button_b.is_pressed():
            elapsed = running_time() - button_b_last_pushed
            # Change volume if the button was pushed twice in quick succession
            if elapsed < VOLUME_CHANGE_WAIT:
                volume = change_volume(volume)
            else:
                show_volume(volume_to_step(volume))
            button_b_last_pushed = running_time()


if __name__ == "__main__":
    main()

# microbit_games

Games in pythin for the BBC micro:bit

## bop_it

A micro:bit take on the Bop It game, using arrows to indicate which of the buttons or logo to press. Tests your reaction time by allowing progressively shorter wait times for you to push the button.

### Installing

Use [uFlash](https://uflash.readthedocs.io/en/latest/) to install on the micro:bit.

Install uFlash

```
pip install uflash
```

Compile and load

```
uflash bop_it.py
```

### Playing

Press the A button to start.

### Testing

Install pytest

```
pip install pytest
```

Run test suite

```
pytest
```

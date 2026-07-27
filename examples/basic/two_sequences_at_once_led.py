# examples/basic/two_sequences_at_once_led.py
#
# Demonstrates: two LED sequences running simultaneously in opposite directions
# API style: call sequence() for each Vspeed object on every loop iteration
# Async equivalent: examples/async/two_sequences_at_once_led.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/
#
# GammaEaseIn/Out matches human eye sensitivity to brightness — use it for LEDs.

import board
import pwmio

from varspeed import Vspeed

MIN = 0
MAX = 55000

led1 = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
led2 = pwmio.PWMOut(board.D4, frequency=5000, duty_cycle=0)

vs1 = Vspeed(init_position=MIN, result="int", debug=False)
vs2 = Vspeed(init_position=MAX, result="int", debug=False)
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)

led1.duty_cycle = vs1.position
led2.duty_cycle = vs2.position

my_sequence1 = [
    (MIN, 1.0, 10, "GammaEaseIn"),
    (MAX, 1.0, 10, "GammaEaseOut"),
]

my_sequence2 = [
    (MAX, 1.0, 10, "GammaEaseOut"),
    (MIN, 1.0, 10, "GammaEaseInOut"),
]

while True:
    position1, _, changed1 = vs1.sequence(my_sequence1, loop_max=0)
    if changed1:
        led1.duty_cycle = position1

    position2, _, changed2 = vs2.sequence(my_sequence2, loop_max=0)
    if changed2:
        led2.duty_cycle = position2

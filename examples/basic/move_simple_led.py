# examples/basic/move_simple_led.py
#
# Demonstrates: fading an LED using move()
# API style: call move() on every loop iteration
# Async equivalent: examples/async/move_simple_led.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/
#
# GammaEaseIn/Out matches human eye sensitivity to brightness — use it for LEDs.

import board
import pwmio

from varspeed import Vspeed

MIN = 0
MAX = 65535

vs = Vspeed(init_position=MIN, result="int", debug=False)
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
led.duty_cycle = MIN

print("fading UP...")
running = True
while running:
    position, running, changed = vs.move(
        new_position=MAX, time_secs=5, steps=100, easing="GammaEaseIn"
    )
    if changed:
        led.duty_cycle = position

print("fading DOWN...")
running = True
while running:
    position, running, changed = vs.move(
        new_position=MIN, time_secs=5, steps=100, easing="GammaEaseOut", delay_start=3.0
    )
    if changed:
        led.duty_cycle = position

print("done, now at " + str(vs.position))

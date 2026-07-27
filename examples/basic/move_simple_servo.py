# examples/basic/move_simple_servo.py
#
# Demonstrates: moving a servo using move()
# API style: call move() on every loop iteration
# Async equivalent: examples/async/move_simple_servo.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/

import board
import pwmio
from adafruit_motor import servo

from varspeed import Vspeed

MIN = 0
MAX = 180

pwm = pwmio.PWMOut(board.D13, duty_cycle=2**15, frequency=50)
my_servo = servo.Servo(pwm)
my_servo.angle = MIN

vs = Vspeed(init_position=MIN, result="int", debug=False)
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

print("moving to " + str(MAX) + "...")
running = True
while running:
    position, running, changed = vs.move(
        new_position=MAX, time_secs=2, steps=180, easing="ExponentialEaseInOut", delay_start=3.0
    )
    if changed:
        my_servo.angle = position

print("moving to " + str(MIN) + "...")
running = True
while running:
    position, running, changed = vs.move(
        new_position=MIN, time_secs=2, steps=180, easing="ExponentialEaseInOut", delay_start=3.0
    )
    if changed:
        my_servo.angle = position

print("done, now at " + str(vs.position))

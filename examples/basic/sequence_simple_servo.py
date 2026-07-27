# examples/basic/sequence_simple_servo.py
#
# Demonstrates: running a sequence of servo moves using sequence()
# API style: call sequence() on every loop iteration
# Async equivalent: examples/async/sequence_simple_servo.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/
#
# The optional fifth element in each tuple is delay_start — seconds to wait
# before starting that move.

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

my_sequence = [
    (MAX, 2.0, 100, "QuadEaseIn"),
    (MIN, 2.0, 100, "QuadEaseOut",   3),  # wait 3 seconds before starting
    (MAX, 2.0, 100, "SineEaseInOut", 2),  # wait 2 seconds before starting
]

print("running sequence...")
running = True
while running:
    position, running, changed = vs.sequence(my_sequence, loop_max=1)
    if changed:
        my_servo.angle = position

print("done, now at " + str(vs.position))

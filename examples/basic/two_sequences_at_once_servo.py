# examples/basic/two_sequences_at_once_servo.py
#
# Demonstrates: two servos running opposite sequences simultaneously
# API style: call sequence() for each Vspeed object on every loop iteration
# Async equivalent: examples/async/two_sequences_at_once_servo.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/

import board
import pwmio
from adafruit_motor import servo

from varspeed import Vspeed

MIN = 15
MAX = 165

pwm1 = pwmio.PWMOut(board.D13, duty_cycle=2**15, frequency=50)
pwm2 = pwmio.PWMOut(board.D4,  duty_cycle=2**15, frequency=50)
my_servo1 = servo.Servo(pwm1)
my_servo2 = servo.Servo(pwm2)

vs1 = Vspeed(init_position=MIN, result="int", debug=False)
vs2 = Vspeed(init_position=MAX, result="int", debug=False)
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)

my_servo1.angle = vs1.position
my_servo2.angle = vs2.position

my_sequence1 = [
    (MIN, 1, 100, "QuadEaseIn", 2),
    (MAX, 1, 100, "QuadEaseIn", 2),
]

my_sequence2 = [
    (MAX, 1, 100, "QuadEaseIn", 2),
    (MIN, 1, 100, "QuadEaseIn", 2),
]

running1 = True
running2 = True
while running1 and running2:
    position1, running1, changed1 = vs1.sequence(my_sequence1, loop_max=3)
    if changed1:
        my_servo1.angle = position1

    position2, running2, changed2 = vs2.sequence(my_sequence2, loop_max=3)
    if changed2:
        my_servo2.angle = position2

print("done")

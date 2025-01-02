# move_simple_servo.py
#
# changes the position of a servo over time

import board
import pwmio
from adafruit_motor import servo
from varspeed import Vspeed

MIN = 0
MAX = 180

# set up the varspeed object
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info
vs = Vspeed(init_position=MIN, result="int", debug=False)
# make the output of the function be within the MIN MAX bounds set
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

# create a PWMOut object on Pin D13
pwm = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)

# Create a servo object
my_servo = servo.Servo(pwm)
# set the servo to a known starting point
my_servo.angle = MIN
print(f'Starting at position {MIN}, in 3 seconds starting move to {MAX}...')

running = True
while running:
    # move(new_position,time_secs of move,steps in move,easing function, delay_start in seconds)
    # for more into on easing, see: https://github.com/semitable/easing-functions
    # for a visual repesentation of the easing options see: https://easings.net
    #
    # move from the current MIN position    
    position, running, changed = vs.move(
        new_position=MAX, time_secs=2, steps=180, easing="ExponentialEaseInOut", delay_start=3.0)
    if changed:  # only act if the output changed
        my_servo.angle = position

running = True
while running:
    # move(new_position,time_secs of move,steps in move,easing function, delay_start in seconds)
    # for more into on easing, see: https://github.com/semitable/easing-functions
    # for a visual repesentation of the easing options see: https://easings.net
    #
    # move from the current MIN position    
    position, running, changed = vs.move(
        new_position=MIN, time_secs=2, steps=180, easing="ExponentialEaseInOut", delay_start=3.0)
    if changed:  # only act if the output changed
        my_servo.angle = position
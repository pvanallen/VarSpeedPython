# move_simple_led.py
#
# changes the brightness of an LED over time

import board
import pwmio
import time

from varspeed import Vspeed

MIN = 0
MAX = 65535
# set up the varspeed object
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info
vs = Vspeed(init_position=MIN, result="int", debug=False)
# make the output of the function be within the bounds set
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

# LED setup for most CircuitPython boards:
led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)

print(f'Starting at value {MIN}, in 3 seconds starting move to {MAX}...')
# set the LED to a known starting point
led.duty_cycle = MIN
time.sleep(3)

running = True
print("fading UP...")
while running:
    # run a move from the current position
    # move(new_position,time_secs of move,steps in move,easing function)
    # for more into on easing, see: https://github.com/semitable/easing-functions
    # for a visual repesentation of the easing options see: https://easings.net
    # NOTE: the names of the easing functions are different on this website
    # THIS EXAMPLE USES A NEW GAMMA EASING FUNCTION WHICH LOOKS BEST FOR LEDS
    position, running, changed = vs.move(
        new_position=MAX, time_secs=5, steps=100, easing="GammaEaseIn")
    if changed:
        led.duty_cycle = int(position)
print(f'Paused for 3 seconds at {position} brightness...')
time.sleep(3)
        
print("fading DOWN....")
running = True
while running:
    position, running, changed = vs.move(
        new_position=MIN, time_secs=5, steps=100, easing="GammaEaseOut",delay_start=3.0)
    if changed:
        led.duty_cycle = int(position)

print(f'Now at {position} brightness...')
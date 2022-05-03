import board
import digitalio
import pwmio
import time

from varspeed import Vspeed

MIN = 0
MAX = 65535
# set up the varspeed object
#
# init_position = initial start position
# result = float, int
vs = Vspeed(init_position=MIN, result="int")
# make the output of the function be within the bounds set
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

# LED setup for most CircuitPython boards:
led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)

running = True
while running:
    # run a move from the current position
    # move(new_position,time_secs of move,steps in move,easing function)
    position, running, changed = vs.move(
        new_position=MAX, time_secs=2, steps=100, easing="QuadEaseInOut")
    if changed:
        print(f'Step: {vs.step}, Position: {position}')
        led.duty_cycle = int(position / 100)

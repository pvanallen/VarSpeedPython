# two_sequences_at_once_led.py
#
# an example of how to use two sequences at the same time without blocking either one
#
import board
import digitalio
import pwmio
import time
from varspeed import Vspeed

MIN = 0
# max = 65535 # the brightest it can go
MAX = 55000  # higher than this isn't much brighter

# create a PWMOut object on Pin D2
led1 = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
# create a PWMOut object on Pin D3
led2 = pwmio.PWMOut(board.D4, frequency=5000, duty_cycle=0)

# set up the varspeed objects
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info
vs1 = Vspeed(init_position=MIN, result="int", debug=False)
vs2 = Vspeed(init_position=MAX, result="int", debug=False)
# make the output of the function be within the bounds set
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)

# set the LED to a known starting point
led1.duty_cycle = vs1.position
led2.duty_cycle = vs2.position

my_sequence1 = [(MIN, 1.0, 10, "GammaEaseIn"),
                (MAX, 1.0, 10, "GammaEaseOut")]

my_sequence2 = [(MAX, 1.0, 10, "GammaEaseOut"),
                (MIN, 1.0, 10, "GammaEaseInOut")]

running1 = True
running2 = True
#print("starting  position",vs.position)
while running1 and running2:
    # run two sequences of moves at the same time
    # sequence(sequence,loop,loop_max)
    # sequence = moves in this format: (next-position,secs-to-move,number-of-steps,easing function) example: [(90,5,10,LinearInOut),(0,8,10,QuadEaseInOut),(180,5,10,CubicEaseIn)]
    # loop_max = number of times to run the sequence in a loop
    #     if zero, loop forever
    #     if 1, play once
    #     if >1, loop sequence that many times
    #
    position1, running1, changed1 = vs1.sequence(
        sequence=my_sequence1, loop_max=0)
    if changed1:
        #print(f'Sequence Num: {vs1.seq_pos}, Step: {vs1.step}, Position: {position1}')
        led1.duty_cycle = position1

    position2, running2, changed2 = vs2.sequence(
            sequence=my_sequence2, loop_max=0)
    if changed2:
        #print(f'Sequence Num: {vs2.seq_pos}, Step: {vs2.step}, Position: {position2}')
        led2.duty_cycle = position2

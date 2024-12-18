# sequence_simple.py
#
# a non-hardware dependent example of using the VarSpeedPython class
# to have a series of moves in a sequence
#
import time

from varspeed import Vspeed

MIN = 0.0
MAX = 100.0

# set up the varspeed object
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info
vs = Vspeed(init_position=MAX, result="int", debug=False)
# make the output of the function be within the bounds set
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

my_sequence = [(MAX / 2, 3.0, 10, "QuadEaseIn"),
               (MIN, 3.0, 10, "QuadEaseOut"),
               (MAX, 3.0, 10, "SineEaseInOut")]

running = True
#print("starting  position",vs.position)
while running:
  # run a sequence of moves
  # sequence(sequence,loop,loop_max)
  # sequence = moves in this format: (next-position,secs-to-move,number-of-steps,easing function) example: [(90,5,10,LinearInOut),(0,8,10,QuadEaseInOut),(180,5,10,CubicEaseIn)]
  # loop_max = number of times to run the sequence in a loop
  #     if zero, loop forever
  #     if 1, play once
  #     if >1, loop sequence that many times
  #
    position, running, changed = vs.sequence(sequence=my_sequence, loop_max=2)

  #print(position, running, changed)
    if changed:
        print(
            f'Sequence Num: {vs.seq_pos}, Step: {vs.step}, Position: {position}')

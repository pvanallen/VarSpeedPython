# two_sequences_at_once.py
#
# runs two sequences in parallel without interfering with each another
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
vs1 = Vspeed(init_position=MAX, result="int", debug=False)
vs2 = Vspeed(init_position=MAX, result="int", debug=False)

# create the sequences
my_sequence1 = [(MIN, 1.0, 10, "QuadEaseIn"),
                (MAX, 1.0, 10, "QuadEaseOut")]

my_sequence2 = [(MAX, 1.0, 10, "QuadEaseOut"),
                (MIN, 1.0, 10, "QuadEaseIn")]

running1 = True
running2 = True
#print("starting position",vs.position)
while running1 and running2:
    # run a sequence of moves
    # sequence(sequence,loop,loop_max)
    # sequence = moves in this format: (next-position,secs-to-move,number-of-steps,easing function)
    #     example: [(90,5,10,LinearInOut),(0,8,10,QuadEaseInOut),(180,5,10,CubicEaseIn)]
    # loop_max = number of times to run the sequence in a loop
    #     if zero, loop forever
    #     if 1, play once
    #     if >1, loop sequence that many times
    #
    position1, running1, changed1 = vs1.sequence(
        sequence=my_sequence1, loop_max=2)
    if changed1:
        print(
            f'Sequence 1 Move: {vs1.seq_pos}, Step: {vs1.step}, Position: {position1}')

    position2, running2, changed2 = vs2.sequence(
        sequence=my_sequence2, loop_max=2)
    if changed2:
        print(
            f'Sequence 2 Move: {vs2.seq_pos}, Step: {vs2.step}, Position: {position2}')

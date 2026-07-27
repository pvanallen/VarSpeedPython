# examples/basic/two_sequences_at_once.py
#
# Demonstrates: two sequences running simultaneously — no hardware needed
# API style: call sequence() for each Vspeed object on every loop iteration
# Async equivalent: examples/async/two_sequences_at_once.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/
#
# Because move() and sequence() are non-blocking, calling them for multiple
# Vspeed objects in the same loop runs them in parallel.

from varspeed import Vspeed

MIN = 0
MAX = 100

vs1 = Vspeed(init_position=MAX, result="int", debug=False)
vs2 = Vspeed(init_position=MIN, result="int", debug=False)

my_sequence1 = [
    (MIN, 1.0, 10, "QuadEaseIn"),
    (MAX, 1.0, 10, "QuadEaseOut"),
]

my_sequence2 = [
    (MAX, 1.0, 10, "QuadEaseOut"),
    (MIN, 1.0, 10, "QuadEaseIn"),
]

running1 = True
running2 = True
while running1 and running2:
    position1, running1, changed1 = vs1.sequence(my_sequence1, loop_max=2)
    if changed1:
        print("seq1: " + str(position1))

    position2, running2, changed2 = vs2.sequence(my_sequence2, loop_max=2)
    if changed2:
        print("seq2: " + str(position2))

print("done")

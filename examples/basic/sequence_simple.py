# examples/basic/sequence_simple.py
#
# Demonstrates: running a sequence of moves using sequence() — no hardware needed
# API style: call sequence() on every loop iteration
# Async equivalent: examples/async/sequence_simple.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/
#
# sequence() steps through each move in the list in order, looping if requested.
# Each tuple is: (target_position, time_secs, steps, easing_name)

from varspeed import Vspeed

MIN = 0
MAX = 100

vs = Vspeed(init_position=MIN, result="int", debug=False)

my_sequence = [
    (100, 2.0, 20, "QuadEaseIn"),
    (0,   2.0, 20, "QuadEaseOut"),
    (50,  1.0, 10, "LinearInOut"),
]

print("running sequence...")
running = True
while running:
    position, running, changed = vs.sequence(my_sequence, loop_max=2)
    if changed:
        print(position)

print("done")

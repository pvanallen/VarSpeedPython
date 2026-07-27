# examples/basic/move_simple.py
#
# Demonstrates: a simple move using move() — no hardware needed
# API style: call move() on every loop iteration
# Async equivalent: examples/async/move_simple.py
# Easing reference: https://philvanallen.com/easings_cheatsheet/
#
# move() returns (position, running, changed). Call it in a while loop
# until running is False — each call advances the move by one step.

from varspeed import Vspeed

MIN = 0
MAX = 100

vs = Vspeed(init_position=MIN, result="int", debug=False)

print("moving to " + str(MAX) + "...")
running = True
while running:
    position, running, changed = vs.move(
        new_position=MAX, time_secs=2.0, steps=20, easing="LinearInOut"
    )
    if changed:
        print(position)

print("done, now at " + str(vs.position))

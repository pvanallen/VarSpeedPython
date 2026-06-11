# examples/async/sequence_simple.py
#
# Demonstrates: running a sequence of moves using sequence() — no hardware needed
# API style: async for loop (sequence)
# Sync equivalent: examples/basic/sequence_simple.py
#
# sequence() steps through each move in the list in order, looping if requested.
# Each tuple is: (target_position, time_secs, steps, easing_name)
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio

from varspeed import Vspeed

vs = Vspeed(init_position=0, result="float", debug=False)

my_sequence = [
    (100, 2.0, 20, "QuadEaseIn"),
    (0,   2.0, 20, "QuadEaseOut"),
    (50,  1.0, 10, "LinearInOut"),
]


async def main():
    print("running sequence...")
    async for position, running, changed in vs.sequence(my_sequence, loop_max=2):
        if changed:
            print(position)

    print("done")


asyncio.run(main())

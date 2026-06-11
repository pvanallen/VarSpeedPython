# examples/async/two_sequences_at_once.py
#
# Demonstrates: two sequences running concurrently — no hardware needed
# API style: async for loop (sequence) with asyncio.gather()
# Sync equivalent: examples/basic/two_sequences_at_once.py
#
# asyncio.gather() runs both coroutines at the same time. Each one yields
# control during its sleep, letting the other advance — without threading.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio

from varspeed import Vspeed

vs1 = Vspeed(init_position=0,   result="float", debug=False)
vs2 = Vspeed(init_position=100, result="float", debug=False)

seq1 = [
    (100, 2.0, 20, "QuadEaseIn"),
    (0,   2.0, 20, "QuadEaseOut"),
]
seq2 = [
    (0,   3.0, 30, "SineEaseInOut"),
    (100, 3.0, 30, "SineEaseInOut"),
]


async def run_actuator(vs, sequence, label):
    async for position, running, changed in vs.sequence(sequence, loop_max=1):
        if changed:
            print(label + ": " + str(round(position, 1)))


async def main():
    await asyncio.gather(
        run_actuator(vs1, seq1, "A"),
        run_actuator(vs2, seq2, "B"),
    )
    print("both done")


asyncio.run(main())

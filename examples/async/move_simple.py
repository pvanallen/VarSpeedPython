# examples/async/move_simple.py
#
# Demonstrates: a simple move using move_all() — no hardware needed
# API style: async for loop (move_all)
# Sync equivalent: examples/basic/move_simple.py
#
# move_all() steps through every step of the move, yielding at each one.
# Awaiting each step lets other coroutines run — this is how concurrent
# actuators become possible.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio

from varspeed import Vspeed

vs = Vspeed(init_position=0, result="float", debug=False)


async def main():
    print("moving to 100...")
    async for position, running, changed in vs.move_all(
        new_position=100, time_secs=2.0, steps=20, easing="LinearInOut"
    ):
        if changed:
            print(position)

    print("done, now at " + str(vs.position))


asyncio.run(main())

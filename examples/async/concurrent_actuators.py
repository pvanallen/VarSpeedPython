# examples/async/concurrent_actuators.py
#
# Demonstrates: two actuators moving concurrently with different speeds and easings
# API style: async for loop (move) with asyncio.create_task()
# Sync equivalent: not possible — concurrent motion is the main reason to use async
#
# Each run_actuator() coroutine drives one Vspeed object through a single move.
# create_task() starts both at the same time. Because move() uses
# asyncio.sleep() between steps, each task yields control to the other
# while it waits — no threading required.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio

from varspeed.varspeed_async import Vspeed

vs_a = Vspeed(init_position=0,   result="float", debug=False)
vs_b = Vspeed(init_position=100, result="float", debug=False)


async def run_actuator(vs, target, time_secs, steps, easing, label):
    """Step through a single move and print each changed value."""
    async for position, running, changed in vs.move(
        new_position=target, time_secs=time_secs, steps=steps, easing=easing
    ):
        if changed:
            print(label + ": " + str(round(position, 1)))
    print(label + " done at " + str(vs.position))


async def main():
    # Both moves start at the same moment and run independently.
    # Naming each task makes it clear what is running concurrently.
    task_a = asyncio.create_task(run_actuator(vs_a, 100, time_secs=3.0, steps=30, easing="QuadEaseIn",    label="A"))
    task_b = asyncio.create_task(run_actuator(vs_b,   0, time_secs=5.0, steps=50, easing="SineEaseInOut", label="B"))
    await task_a
    await task_b
    print("both done")


asyncio.run(main())

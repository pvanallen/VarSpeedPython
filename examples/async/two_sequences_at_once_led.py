# examples/async/two_sequences_at_once_led.py
#
# Demonstrates: two LEDs pulsing in opposite phase simultaneously
# API style: async for loop (sequence) with asyncio.create_task()
# Sync equivalent: examples/basic/two_sequences_at_once_led.py
#
# LED 1 fades up while LED 2 fades down, then vice versa — looping forever.
# create_task() starts each coroutine as a named task running concurrently.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio

from varspeed.varspeed_async import Vspeed

MIN = 0
MAX = 65535  # higher than 55000 isn't noticeably brighter for most LEDs

vs1 = Vspeed(init_position=MIN, result="int", debug=False)
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)

vs2 = Vspeed(init_position=MAX, result="int", debug=False)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)

led1 = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
led2 = pwmio.PWMOut(board.D3, frequency=5000, duty_cycle=0)
led1.duty_cycle = MIN
led2.duty_cycle = MAX

seq1 = [
    (MAX, 3.0, 60, "SineEaseInOut"),
    (MIN, 3.0, 60, "SineEaseInOut"),
]
seq2 = [
    (MIN, 3.0, 60, "SineEaseInOut"),
    (MAX, 3.0, 60, "SineEaseInOut"),
]


async def run_actuator(vs, sequence, led):
    # loop_max=0 means loop forever
    async for position, running, changed in vs.sequence(sequence, loop_max=0):
        if changed:
            led.duty_cycle = position


async def main():
    task_led1 = asyncio.create_task(run_actuator(vs1, seq1, led1))
    task_led2 = asyncio.create_task(run_actuator(vs2, seq2, led2))
    await task_led1
    await task_led2


asyncio.run(main())

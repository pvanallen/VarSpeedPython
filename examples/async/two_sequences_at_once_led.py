# examples/async/two_sequences_at_once_led.py
#
# Demonstrates: two LEDs pulsing in opposite phase simultaneously
# API style: async for loop (sequence) with asyncio.gather()
# Sync equivalent: examples/basic/two_sequences_at_once_led.py
#
# LED 1 fades up while LED 2 fades down, then vice versa — looping forever.
# asyncio.gather() keeps both running in the same event loop without threading.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio

from varspeed import Vspeed

MIN = 0
MAX = 55000

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
    await asyncio.gather(
        run_actuator(vs1, seq1, led1),
        run_actuator(vs2, seq2, led2),
    )


asyncio.run(main())

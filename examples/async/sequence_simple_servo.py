# examples/async/sequence_simple_servo.py
#
# Demonstrates: running a servo through a sequence of moves using sequence()
# API style: async for loop (sequence)
# Sync equivalent: examples/basic/sequence_simple_servo.py
#
# Each tuple: (target_degrees, time_secs, steps, easing[, delay_start])
# delay_start (5th element, optional) pauses before that move begins.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio
from adafruit_motor import servo

from varspeed.varspeed_async import Vspeed

MIN = 0
MAX = 180

vs = Vspeed(init_position=MIN, result="int", debug=False)
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

pwm = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)
my_servo.angle = MIN

my_sequence = [
    (180, 3.0, 60, "SineEaseInOut"),
    (90,  2.0, 40, "QuadEaseOut",  1.0),
    (0,   3.0, 60, "SineEaseInOut"),
]


async def main():
    print("running servo sequence...")
    async for position, running, changed in vs.sequence(my_sequence, loop_max=1):
        if changed:
            my_servo.angle = position

    print("done, now at " + str(vs.position) + " degrees")


asyncio.run(main())

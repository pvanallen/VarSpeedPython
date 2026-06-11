# examples/async/move_simple_servo.py
#
# Demonstrates: sweeping a servo out then back using async move_all()
# API style: async for loop (move_all)
# Sync equivalent: examples/basic/move_simple_servo.py
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio
from adafruit_motor import servo

from varspeed import Vspeed

MIN = 0
MAX = 180

vs = Vspeed(init_position=MIN, result="int", debug=False)
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

pwm = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)
my_servo.angle = MIN


async def main():
    print("sweeping OUT...")
    async for position, running, changed in vs.move_all(
        new_position=MAX, time_secs=3, steps=180, easing="SineEaseInOut"
    ):
        if changed:
            my_servo.angle = position

    print("sweeping BACK...")
    async for position, running, changed in vs.move_all(
        new_position=MIN, time_secs=3, steps=180, easing="SineEaseInOut", delay_start=1.0
    ):
        if changed:
            my_servo.angle = position

    print("done, now at " + str(vs.position) + " degrees")


asyncio.run(main())

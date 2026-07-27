# examples/async/move_simple_led.py
#
# Demonstrates: fading an LED up then down using async move()
# API style: async for loop (move)
# Sync equivalent: examples/basic/move_simple_led.py
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio

from varspeed_async import Vspeed

MIN = 0
MAX = 65535  # higher than 55000 isn't noticeably brighter for most LEDs

vs = Vspeed(init_position=MIN, result="int", debug=False)
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
led.duty_cycle = MIN


async def main():
    print("fading UP...")
    # move() steps through the full move, yielding at each step.
    # Awaiting each step lets other coroutines run during the pauses —
    # this is how concurrent actuators become possible.
    async for position, running, changed in vs.move(
        new_position=MAX, time_secs=5, steps=100, easing="GammaEaseIn"
    ):
        if changed:
            led.duty_cycle = position

    print("fading DOWN...")
    # delay_start pauses before the move begins — useful for settling time
    async for position, running, changed in vs.move(
        new_position=MIN, time_secs=5, steps=100, easing="GammaEaseOut", delay_start=3.0
    ):
        if changed:
            led.duty_cycle = position

    print("done, now at " + str(vs.position) + " brightness")


asyncio.run(main())

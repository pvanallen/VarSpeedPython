# examples/async/two_sequences_at_once_servo.py
#
# Demonstrates: two servos sweeping in opposite directions simultaneously
# API style: async for loop (sequence) with asyncio.create_task()
# Sync equivalent: examples/basic/two_sequences_at_once_servo.py
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

vs1 = Vspeed(init_position=MIN, result="int", debug=False)
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)

vs2 = Vspeed(init_position=MAX, result="int", debug=False)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)

pwm1 = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.D12, duty_cycle=2 ** 15, frequency=50)
servo1 = servo.Servo(pwm1)
servo2 = servo.Servo(pwm2)
servo1.angle = MIN
servo2.angle = MAX

seq1 = [
    (MAX, 4.0, 80, "SineEaseInOut"),
    (MIN, 4.0, 80, "SineEaseInOut"),
]
seq2 = [
    (MIN, 4.0, 80, "SineEaseInOut"),
    (MAX, 4.0, 80, "SineEaseInOut"),
]


async def run_actuator(vs, sequence, my_servo):
    async for position, running, changed in vs.sequence(sequence, loop_max=0):
        if changed:
            my_servo.angle = position


async def main():
    task_servo1 = asyncio.create_task(run_actuator(vs1, seq1, servo1))
    task_servo2 = asyncio.create_task(run_actuator(vs2, seq2, servo2))
    await task_servo1
    await task_servo2


asyncio.run(main())

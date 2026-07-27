# examples/async/concurrent_sequences.py
#
# Demonstrates: a servo and an LED each running their own sequence simultaneously
# API style: async for loop (sequence) with asyncio.create_task()
# Sync equivalent: not possible — concurrent sequences require async
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio
from adafruit_motor import servo

from varspeed_async import Vspeed

SERVO_MIN = 0
SERVO_MAX = 180
LED_MIN   = 0
LED_MAX   = 65535  # higher than 55000 isn't noticeably brighter for most LEDs

vs_servo = Vspeed(init_position=SERVO_MIN, result="int", debug=False)
vs_servo.set_bounds(lower_bound=SERVO_MIN, upper_bound=SERVO_MAX)

vs_led = Vspeed(init_position=LED_MIN, result="int", debug=False)
vs_led.set_bounds(lower_bound=LED_MIN, upper_bound=LED_MAX)

pwm_servo = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
my_servo  = servo.Servo(pwm_servo)
my_servo.angle = SERVO_MIN

pwm_led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
pwm_led.duty_cycle = LED_MIN

servo_seq = [
    (SERVO_MAX, 4.0, 80, "SineEaseInOut"),
    (SERVO_MIN, 4.0, 80, "SineEaseInOut"),
]
led_seq = [
    (LED_MAX, 2.0, 40, "GammaEaseIn"),
    (LED_MIN, 2.0, 40, "GammaEaseOut", 1.0),
]


async def run_actuator(vs, sequence, label):
    async for position, running, changed in vs.sequence(sequence, loop_max=0):
        if changed:
            if label == "servo":
                my_servo.angle = position
            else:
                pwm_led.duty_cycle = position


async def main():
    task_servo = asyncio.create_task(run_actuator(vs_servo, servo_seq, "servo"))
    task_led   = asyncio.create_task(run_actuator(vs_led,   led_seq,   "led"))
    await task_servo
    await task_led


asyncio.run(main())

# examples/async/move_servo_and_led.py
#
# Demonstrates: moving a servo and fading an LED at the same time
# API style: generator style (move_all) with asyncio.gather()
# Sync equivalent: not possible — concurrent motion is the main reason to use async
#
# The servo sweeps 0 -> 180 degrees while the LED fades off -> on,
# both running simultaneously in the same event loop.
#
# CircuitPython note: asyncio.run(main()) works with adafruit_asyncio v3+.
# On older CircuitPython, use: asyncio.get_event_loop().run_until_complete(main())

import asyncio
import board
import pwmio
from adafruit_motor import servo

from varspeed import Vspeed

# Servo range in degrees
SERVO_MIN = 0
SERVO_MAX = 180

# LED PWM range — 55000 is roughly full brightness for most LEDs
LED_MIN = 0
LED_MAX = 55000

vs_servo = Vspeed(init_position=SERVO_MIN, result="int", debug=False)
vs_servo.set_bounds(lower_bound=SERVO_MIN, upper_bound=SERVO_MAX)

vs_led = Vspeed(init_position=LED_MIN, result="int", debug=False)
vs_led.set_bounds(lower_bound=LED_MIN, upper_bound=LED_MAX)

pwm_servo = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm_servo)
my_servo.angle = SERVO_MIN

pwm_led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
pwm_led.duty_cycle = LED_MIN


async def run_actuator(vs, target, time_secs, steps, easing, label):
    """Step through a move and return the final position."""
    print("moving in...")
    async for position, running, changed in vs.move_all(
        new_position=target, time_secs=time_secs, steps=steps, easing=easing
    ):
        if changed:
            if label == "servo":
                my_servo.angle = position
            else:
                pwm_led.duty_cycle = position
    print(label + " done at " + str(vs.position))


async def main():
    print("moving out...")
    # asyncio.gather() runs both coroutines at the same time.
    # Each one yields control during its sleep, letting the other advance.
    await asyncio.gather(
        run_actuator(vs_servo, SERVO_MAX, time_secs=3, steps=180,
                     easing="SineEaseInOut", label="servo"),
        run_actuator(vs_led,   LED_MAX,   time_secs=6, steps=100,
                     easing="GammaEaseIn",  label="led"),
    )

    print("returning...")
    await asyncio.gather(
        run_actuator(vs_servo, SERVO_MIN, time_secs=6, steps=180,
                     easing="SineEaseInOut", label="servo"),
        run_actuator(vs_led,   LED_MIN,   time_secs=3, steps=100,
                     easing="GammaEaseOut", label="led"),
    )
    print("both done")


asyncio.run(main())

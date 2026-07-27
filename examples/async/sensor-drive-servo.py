import asyncio

import analogio
import board
import pwmio
from adafruit_motor import servo

from varspeed.varspeed_async import Vspeed, map_range

state = {}
SERVO_MIN = 0
SERVO_MAX = 180
SENSOR_MIN = 0
SENSOR_MAX = 65535
POLL_INTERVAL = 0.05
RUN_TIME = 30


async def init():
    print("starting...")
    state["analog_in"] = analogio.AnalogIn(board.A0)
    state["pwm"] = pwmio.PWMOut(board.D13, duty_cycle=2**15, frequency=50)
    state["servo"] = servo.Servo(state["pwm"])
    state["servo"].angle = SERVO_MIN
    state["sensor_value"] = 0


async def watch_sensor(name, delay):
    try:
        while True:
            value = state["analog_in"].value
            state["sensor_value"] = map_range(
                value, SENSOR_MIN, SENSOR_MAX, SERVO_MIN, SERVO_MAX, result="int"
            )
            await asyncio.sleep(delay)
    finally:
        print(name, "done")


async def move_servo(name, delay):
    try:
        while True:
            value = state["sensor_value"]
            state["servo"].angle = value
            print(name, value)
            await asyncio.sleep(delay)
    finally:
        print(name, "done")


async def main():
    await init()

    task1 = asyncio.create_task(watch_sensor("sensor", POLL_INTERVAL))
    task2 = asyncio.create_task(move_servo("servo", POLL_INTERVAL))
    try:
        await asyncio.sleep(RUN_TIME)
    finally:
        print("cancelling")
        task1.cancel()
        task2.cancel()
        await asyncio.sleep(0)
        state["pwm"].deinit()
        state["analog_in"].deinit()


asyncio.run(main())

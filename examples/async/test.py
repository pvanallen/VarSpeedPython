import asyncio
import time

import analogio
import board
import pwmio
from adafruit_motor import servo

from varspeed.varspeed_async import Vspeed, map_range

# --- constants ---
SERVO_MIN = 0
SERVO_MAX = 180
SENSOR_MIN = 0
SENSOR_MAX = 65535
POLL_INTERVAL = 0.05
EXIT_THRESHOLD = 200
EXIT_TIMEOUT = 4.0

# --- varspeed ---
vs = Vspeed(init_position=0, result="int", debug=False)

# --- sequences ---
my_sequence1 = [
    (160, 0.5, 200, "QuadEaseIn"),
    (140, 0.5, 200, "QuadEaseOut"),
]

my_sequence2 = [
    (0, 0.5, 200, "QuadEaseIn"),
    (20, 0.5, 200, "QuadEaseOut"),
]

# --- state ---
state = {}
exit_event = asyncio.Event()


# --- tasks ---
async def watch_sensor(name, delay):
    low_since = None
    try:
        while True:
            state["sensor_value"] = state["analog_in"].value
            prev = state["sequence"]
            state["sequence"] = (
                my_sequence1 if state["sensor_value"] > SENSOR_MAX / 2 else my_sequence2
            )

            if state["sensor_value"] <= EXIT_THRESHOLD:
                if low_since is None:
                    low_since = time.monotonic()
                elif time.monotonic() - low_since >= EXIT_TIMEOUT:
                    print("sensor low for " + str(EXIT_TIMEOUT) + "s — exiting")
                    exit_event.set()
                    return
            else:
                low_since = None

            await asyncio.sleep(delay)
    finally:
        print(name, "done")


async def run_sequence():
    current = state["sequence"]
    async for position, running, changed in vs.sequence(current, loop_max=0):
        if state["sequence"] is not current:
            print("switching sequence", state["sequence"])
            return
        if exit_event.is_set():
            return
        if changed:
            state["servo"].angle = position
            print(position)


# --- init ---
async def init():
    print("starting...")
    state["analog_in"] = analogio.AnalogIn(board.A0)
    state["pwm"] = pwmio.PWMOut(board.D13, duty_cycle=2**15, frequency=50)
    state["servo"] = servo.Servo(state["pwm"], min_pulse=500, max_pulse=2500)
    state["servo"].angle = SERVO_MIN
    state["sensor_value"] = 0
    state["sequence"] = my_sequence1


# --- main ---
async def main():
    await init()

    task_sensor = asyncio.create_task(watch_sensor("analogIn", POLL_INTERVAL))

    try:
        while not exit_event.is_set():
            await run_sequence()
        print("cleaning up...")
    finally:
        task_sensor.cancel()
        await asyncio.sleep(0)
        state["pwm"].deinit()
        state["analog_in"].deinit()


asyncio.run(main())

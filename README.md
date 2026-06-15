# VarSpeedPython library #

## Description

The library is designed for projects that need to control values over time. For example: setting the new angle of a servo in 3.0 seconds; setting the brightness of an LED by fading up in 2.5 seconds; or moving a graphic on a screen. You can set the amount of time for a change in value, and apply easing to each move to make it seem more natural.

It also provides a function for running **sequences** of moves where each move in the sequence has a new position and speed. Sequences can be looped or repeated if desired.

More than one move or sequence can be run at the same time.

VarSpeedPython objects are designed to be called repeatedly and do not block execution. It is compatible with standard Python and CircuitPython (v8.0+ to support asyncio, [more info here](https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/overview)).

This Python library is descended from the VarspeedServo library (https://github.com/netlabtoolkit/VarSpeedServo), originally written for the Arduino in C++ (which was itself built on an early Arduino servo library). Unlike the old Arduino library, VarSpeedPython is not tied to servos, and can be used more generally for timed moves from one value to another. It is also **not** bound to any processor architecture with hardware interrupts etc.

---

> **Sync vs Async — which should I use?**
>
> **Sync** (`varspeed_basic.py`): best for beginners, existing curriculum, or CircuitPython without asyncio. Simple event-loop style — call `move()` on every loop iteration.
>
> **Async** (`varspeed.py`): use when you need concurrent actuators (e.g. a servo and an LED moving independently at the same time), or when you want to learn `async/await` patterns. Requires Python 3.9+ or CircuitPython with `adafruit_asyncio` v3+.

---

<!-- TOC START min:2 max:2 link:true asterisk:false update:true -->
- [Description](#description)
- [Installation](#installation)
- [Quick Start (async — start here)](#quick-start-async--start-here)
- [Quick Start (sync)](#quick-start-sync)
- [API Reference](#api-reference)
- [Easing Types](#easing-types)
- [Examples](#examples)
- [Circuit Python Setup](#circuit-python-setup)
- [Migration: Sync → Async](#migration-sync--async)
<!-- TOC END -->

---

## Installation

**Computer** — For a simple setup, place `varspeed/varspeed.py` and `varspeed/easing_functions.py` in your working directory. Or, install in editable mode from the repo:

```bash
pip install -e .
```

**Device with CircuitPython** — place `varspeed/varspeed.py` and `varspeed/easing_functions.py` in the `CIRCUITPY/lib/` directory, along with the `asyncio` folder from the [Adafruit CircuitPython bundle](https://circuitpython.org/libraries).

---

## Quick Start (async — start here)

```python
import asyncio
from varspeed import Vspeed

vs = Vspeed(init_position=0, result="int")

async def main():
    async for position, running, changed in vs.move(
        new_position=100, time_secs=2.0, steps=20, easing="SineEaseInOut"
    ):
        if changed:
            print(position)  # drive your actuator here

asyncio.run(main())
```

---

## Quick Start (sync)

Uses `varspeed_basic.py` — requires `varspeed_basic import Vspeed`

```python
from varspeed_basic import Vspeed

vs = Vspeed(init_position=0, result="int")

while True:
    position, running, changed = vs.move(new_position=100, time_secs=2.0, steps=20, easing="SineEaseInOut")
    if changed:
        print(position)  # drive your actuator here
    if not running:
        break
```

---

## API Reference

### CLASS: Vspeed
```python
class Vspeed():
```

Provides a non-blocking object that can be called repeatedly from an event loop with the `move()` and `sequence()` functions to generate a timed series of values from a current position to a new position(s).

---

### init
```python
def __init__(self, init_position = 0, result = "int", debug = False):
```

Creates and initializes a Vspeed object.

#### Args
* **init_position** (int/float) : sets the initial position of the object.
* **result** (string = "int" or "float") : sets the type of the returned position.
* **debug** (True/False) : sets debugging mode on or off, resulting in prints on or off.

#### Returns
* **object**  : returns a Vspeed object

---

### move
```python
# sync only — varspeed_basic.py
from varspeed_basic import Vspeed

def move(self, new_position = 0, time_secs = 2.0, steps = 20, easing = "LinearInOut", delay_start = 0.0):
```

Generates a series of values that transition from the current position to a new_position. Call this repeatedly from your event loop.

#### Args
* **new_position** (float or int) : position output will change to over time_secs
* **time_secs** (int) : time for the transition to the new_position
* **steps** (int) : number of steps to change from the start position to the new_position
* **easing** (string) : the easing function to use for the transition
* **delay_start** (float) : the number of seconds to delay the start of the move

#### Returns
* **position** (int or float) : each new position, marked by changed being True
* **running** (Boolean) : if true there are more steps to go in the transition/move
* **changed** (Boolean) : indicates if the latest value is different from the previous value

---

### move (async)
**async only** — requires `varspeed.py`

```python
from varspeed import Vspeed

async for position, running, changed in vs.move(new_position, time_secs, steps, easing):
    ...
```

Async iterator that yields `(position, running, changed)` on every step, sleeping between steps. Replaces the sync `move()` — instead of calling in a loop, use `async for`.

#### Args
Same as `move()` above (`new_position`, `time_secs`, `steps`, `easing`, `delay_start`).

#### Yields
* **position** (int or float) : each new position
* **running** (Boolean) : True if more steps remain
* **changed** (Boolean) : True if the value changed this step

---

### sequence
```python
def sequence(self, sequence, loop_max = 1):
```

Creates a series of values in a sequence of moves as specified in the sequence array. In the async version (`varspeed.py`), this is an async iterator used with `async for`. In the sync version (`varspeed_basic.py`), call it repeatedly from your event loop.

#### Args
* **sequence** (array of tuples) : perform a sequence of moves — each tuple is `(position, time_secs, steps, easing[, delay_start])`.
* **loop_max** (int) : how many times to loop the sequence; zero means loop forever.

#### Returns / Yields
* **position** (int or float) : each new position, marked by changed being True
* **running** (Boolean) : if true there are more steps to go in the transition/move
* **changed** (Boolean) : indicates if the latest position value is different from the previous value

---

### sequence_change_seq_num
```python
def sequence_change_seq_num(self, seq_position = 0):
```

Sets the current sequence number.

#### Args
* **seq_position** (int) : jump to the element in the sequence[seq_position] array.

#### Returns
nothing

---

### sequence_run
```python
def sequence_run(self, value = True):
```

Pauses or unpauses a running sequence.

#### Args
* **value** (Boolean) : pauses (False) or unpauses (True) the run of the sequence.

#### Returns
nothing

---

### set_position
```python
def set_position(self, position = 0):
```

Sets the current position from which the next move will proceed.

#### Args
* **position** (int or float) : sets the current position of the object

#### Returns
nothing

---

### set_bounds
```python
def set_bounds(self, lower_bound = 0, upper_bound = 1000, bounded=True):
```

Sets the lower and upper bounds of values returned by a move or sequence.

#### Args
* **lower_bound** (int) : sets the lower allowed bound of the output of a move or sequence
* **upper_bound** (int) : sets the upper allowed bound of the output of a move or sequence
* **bounded** (Boolean) : turns bounds checking on (True — Default) or off (False)

#### Returns
nothing

---

### map_range
```python
from varspeed import map_range

map_range(value, in_min, in_max, out_min, out_max, result="float")
```

Maps a value from one range to another. Useful for converting sensor readings to actuator ranges.

#### Args
* **value** (int or float) : input value to map
* **in_min** (int or float) : lower bound of the input range
* **in_max** (int or float) : upper bound of the input range
* **out_min** (int or float) : lower bound of the output range
* **out_max** (int or float) : upper bound of the output range
* **result** (string) : `"int"` to return a rounded integer, `"float"` for a float (default)

#### Returns
* **int or float** : the mapped value in the output range

---

## Easing Types

For any move (even within a sequence), you can set an easing function using any of the following classic Robert Penner easing types. For an animated and graphed visualization of each easing type, see [https://philvanallen.com/easings_cheatsheet/](https://philvanallen.com/easings_cheatsheet/). 

For an explanation of the use of easing, see this article: [Animation Principles in UI Design: Understanding Easing](https://medium.com/motion-in-interaction/animation-principles-in-ui-design-understanding-easing-bea05243fe3)

Easing names in this library start with the family name (e.g. `Linear`, `Quad`, `Cubic`) followed by `Ease` and the direction (`In`, `Out`, or `InOut`). For example, `CubicEaseInOut`. The Gamma functions are unique to this library and not found on other easing references.

* LinearInOut (essentially no easing)
* QuadEaseInOut, QuadEaseIn, QuadEaseOut
* CubicEaseIn, CubicEaseOut, CubicEaseInOut
* QuarticEaseIn, QuarticEaseOut, QuarticEaseInOut
* QuinticEaseIn, QuinticEaseOut, QuinticEaseInOut
* SineEaseIn, SineEaseOut, SineEaseInOut
* CircularEaseIn, CircularEaseOut, CircularEaseInOut
* ExponentialEaseIn, ExponentialEaseOut, ExponentialEaseInOut
* ElasticEaseIn, ElasticEaseOut, ElasticEaseInOut
* BackEaseIn, BackEaseOut, BackEaseInOut
* BounceEaseIn, BounceEaseOut, BounceEaseInOut
* GammaEaseIn, GammaEaseOut, GammaEaseInOut

* **GAMMA EASING NOTES** - provides gamma correction of 2.8 for dimming LEDs and other lighting to match human vision characteristics. **EXPLANATION** of gamma correction: https://www.advateklighting.com/blog/guides/dithering-and-gamma-correction

---

## Examples

### Async examples

**async only** — requires `varspeed.py` (`from varspeed import Vspeed`)

* **[async/move_simple.py](examples/async/move_simple.py)** — minimal async move, no hardware
* **[async/move_simple_led.py](examples/async/move_simple_led.py)** — fade an LED asynchronously
* **[async/move_simple_servo.py](examples/async/move_simple_servo.py)** — move a servo asynchronously
* **[async/sequence_simple.py](examples/async/sequence_simple.py)** — run a sequence asynchronously, no hardware
* **[async/sequence_simple_servo.py](examples/async/sequence_simple_servo.py)** — sequence of servo moves
* **[async/two_sequences_at_once.py](examples/async/two_sequences_at_once.py)** — two sequences running simultaneously, no hardware
* **[async/two_sequences_at_once_led.py](examples/async/two_sequences_at_once_led.py)** — two LED sequences simultaneously
* **[async/two_sequences_at_once_servo.py](examples/async/two_sequences_at_once_servo.py)** — two servos running opposite sequences
* **[async/concurrent_actuators.py](examples/async/concurrent_actuators.py)** — two actuators with different speeds and easings
* **[async/concurrent_sequences.py](examples/async/concurrent_sequences.py)** — a servo and LED each running their own sequence
* **[async/move_servo_and_led.py](examples/async/move_servo_and_led.py)** — servo and LED moving simultaneously
* **[async/sensor-drive-servo.py](examples/async/sensor-drive-servo.py)** — read an analog sensor and drive a servo concurrently

### Sync examples

Uses `varspeed_basic.py` (`from varspeed_basic import Vspeed`)

* **[basic/move_simple.py](examples/basic/move_simple.py)** — a non-CircuitPython dependent example that can be run in any Python environment
* **[basic/sequence_simple.py](examples/basic/sequence_simple.py)** — a non-CircuitPython dependent example that can be run in any Python environment
* **[basic/move_simple_led.py](examples/basic/move_simple_led.py)** — changes the brightness of an LED
* **[basic/move_simple_servo.py](examples/basic/move_simple_servo.py)** — changes the angle of a servo
* **[basic/sequence_simple_servo.py](examples/basic/sequence_simple_servo.py)** — runs a sequence of moves for a servo
* **[basic/two_sequences_at_once_led.py](examples/basic/two_sequences_at_once_led.py)** — shows how to do two sequences simultaneously, for example dimming two LEDs in opposite directions
* **[basic/two_sequences_at_once_servo.py](examples/basic/two_sequences_at_once_servo.py)** — runs different sequences for two servos simultaneously

---

## Circuit Python Setup

To set up on a CircuitPython hardware device:

* Put `varspeed/varspeed.py` in the **lib** directory on CIRCUITPY (async version) **or** `varspeed/varspeed_basic.py` (sync version)
* Put `varspeed/easing_functions.py` in the **lib** directory on CIRCUITPY
* Put the asyncio library from the [CircuitPython Library bundle](https://circuitpython.org/libraries) in the **lib** directory on CIRCUITPY
* Copy the python code from any of the examples into `code.py` or `main.py` at the top of CIRCUITPY

---

## Migration: Sync → Async

If you have existing sync code and want to move to the async version, here is the key change:

**Before (sync):**
```python
from varspeed_basic import Vspeed

vs = Vspeed(init_position=0, result="int")

while True:
    position, running, changed = vs.move(new_position=100, time_secs=2.0, steps=20, easing="SineEaseInOut")
    if changed:
        print(position)
    if not running:
        break
```

**After (async):**
```python
import asyncio
from varspeed import Vspeed

vs = Vspeed(init_position=0, result="int")

async def main():
    async for position, running, changed in vs.move(
        new_position=100, time_secs=2.0, steps=20, easing="SineEaseInOut"
    ):
        if changed:
            print(position)

asyncio.run(main())
```

Key differences for the new async version:
- `move()` is now an async iterator — use `async for` instead of calling it in a while loop
- Wrap logic in `async def main()` and call with `asyncio.run(main())`
- `sequence()` works with `async for` in the same way
- Use `asyncio.create_task()` to run multiple actuators concurrently — this is the main reason to migrate

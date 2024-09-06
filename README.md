# VarSpeedPython library #

## Description
This Python library is descended from the VarspeedServo library (https://github.com/netlabtoolkit/VarSpeedServo), originally written for the Arduino in C++ (which was itself built on an early Arduino servo library). Unlike the old Arduino library, VarSpeedPython is not tied to servos, and can be used more generally for timed moves from one value to another. It is also **not** bound to any processor architecture with hardware interrupts etc.

The library is designed for projects that need to control values over time. For example: setting the new angle of a servo in 1.5 seconds; setting the brightness of an LED by fading up; or moving a graphic on a screen. You can set the amount of time for a change in value, and apply easing to each move. It also provides a function for running sequences of moves (that can be looped or repeated if desired), where each move in the sequence has a new position and speed. More than one move or sequence can be run at the same time.

VarSpeedPython objects are designed to be called repeatedly from within an event loop and do not block execution.

<!-- TOC START min:2 max:2 link:true asterisk:false update:true -->
- [Description](#description)
- [Circuit Python Setup](#circuit-python-setup)
- [Code Examples - non-CircuitPython](#code-examples---non-circuitpython)
- [Code Examples - CircuitPython](#code-examples---circuitpython)
- [Easing Types](#easing-types)
- [CLASS: Vspeed](#class-vspeed)
- [init](#init)
- [move](#move)
- [sequence](#sequence)
- [sequence_change_seq_num](#sequence_change_seq_num)
- [sequence_run](#sequence_run)
- [set_position](#set_position)
- [set_bounds](#set_bounds)
<!-- TOC END -->

## Circuit Python Setup

To set up on CircuitPython:

* Put varspeed.py in the lib directory on CIRCUITPY
* Put easing_functions.py in the lib directory on CIRCUITPY
* Copy the python from any of the examples into code.py at the top of CIRCUITPY

## Code Examples - non-CircuitPython

* **[move_simple.py](examples/move_simple.py)** — a non-CircuitPython dependent example that can be run in any Python environment
* **[sequence_simple.py](examples/sequence_simple.py)** — a non-CircuitPython dependent example that can be run in any Python environment

## Code Examples - CircuitPython

* **[move_simple_led.py](examples/move_simple_led.py)** — changes the brightness of an LED
* **[move_simple_servo.py](examples/move_simple_servo.py)** — changes the angle of a servo
* **[sequence_simple_servo.py](examples/sequence_simple_servo.py)** — runs a sequence of moves for a servo
* **[two_sequences_at_once_led.py](examples/two_sequences_at_once_led.py)** — shows how to do two sequences simultaneously, for example dimming two LEDs in opposite directions
* **[two_sequences_at_once_servo.py](examples/two_sequences_at_once_servo.py)** — runs different sequences for two servos simultaneously

## Easing Types

For any move (even within a sequence), you can set an easing function using the following classic Robert Penner easing types. For an animated and graphed visualization of each easing type, see https://easings.net. For an explanation of the use of easing, see this article: [Animation Principles in UI Design: Understanding Easing](https://medium.com/motion-in-interaction/animation-principles-in-ui-design-understanding-easing-bea05243fe3)

> [!WARNING]  
> The names on https://easings.net do not reflect the names used in the `easing_functions.py` file. The names used in this project start with the type of easing used by the function (e.g Linear, Quad, Circular) followed by the word _Ease_ and finally whether it's "In", "Out" or "InOut". For example: the function listed on the website as _easeInOutCubic_  is called _CubicEaseInOut_ in this library. The reason behind this naming scheme is to be consistent with python classes naming conventions. The list with all easing functions with the correct names is listed here below.

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

## CLASS: Vspeed
```python
class Vspeed():
```

---

Provides a non-blocking object that can be called repeatedly from an event loop with the move() and sequence() functions to generate a timed series of values from a current position to a new position(s)

## init
```python
def __init__(self, init_position = 0, result = "int"):
```

---

Creates and initializes a Vspeed object.

### Args
* **init_position** (int/float) : sets the initial position of the object.
* **result** (string = "int" or "float") : sets the type of the returned position.

### Returns
* **object**  : returns a Vspeed object


## move
```python
def move(self, new_position = 0, time_secs = 2.0, steps = 20, easing = "LinearInOut"):
```

---

Generates a series of values that transition from the current position to a new_position.

### Args
* **new_position** (float or int) : position output will change to over time_secs
* **time_secs** (int) : time for the transition to the new_position
* **steps** (int) : number of steps to change from the start position to the new_position
* **easing** (string) : the easing function to use for the transition

### Returns
* **position** (int or float) : each new position, marked by changed being True
* **running** (Boolean) : if true there are more steps to go in the transition/move
* **changed** (Boolean) : indicates if the latest value is different from the previous value

## sequence
```python
def sequence(self, sequence, loop_max = 1):
```

---

Creates a series of values in a sequence of moves as specified in the sequence array.

### Args
* **sequence** (array of tuples) : perform a sequence of moves (position,time,steps,easing) in the array.
* **loop_max** (int) : how many times to loop the sequence, zero means loop forever.

### Returns
* **position** (int or float) : each new position, marked by changed being True
* **running** (Boolean) : if true there are more steps to go in the transition/move
* **changed** (Boolean) : indicates if the latest position value is different from the previous value

## sequence_change_seq_num
```python
def sequence_change_seq_num(self, seq_position = 0):
```

---

Sets the current sequence number.

### Args
* **seq_position** (int) : jump to the element in the sequence[seq_position] array.

### Returns
nothing

## sequence_run
```python
def sequence_run(self, value = True):
```

---

Pauses or unpauses a running sequence.

### Args
* **value** (Boolean) : pauses (False) or unpauses (True) the run of the sequence.

### Returns
nothing

## set_position
```python
def set_position(self, position = 0):
```

---

Sets the current position from which the next move will proceed

### Args
* **position** (int or float) : sets the current position of the object

### Returns
nothing

## set_bounds
```python
def set_bounds(self, lower_bound = 0, upper_bound = 1000, bounded=True):
```

---

Sets the lower and upper bounds of values returned by a move or sequence

### Args
* **lower_bound** (int) : sets the lower allowed bound of the output of a move or sequnce
* **upper_bound** (int) : sets the upper allowed bound of the output of a move or sequnce
* **bounded** (Boolean) : turns bounds checking on (True - Default) or off (False)

### Returns
nothing

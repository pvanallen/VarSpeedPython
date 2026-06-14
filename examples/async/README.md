# Async Examples

These examples use the async version of VarSpeedPython (`varspeed/varspeed.py`).

```python
from varspeed import Vspeed
```

All examples require Python 3.9+ (CPython) or CircuitPython with `adafruit_asyncio` v3+.
Run from the repo root:

```bash
python examples/async/move_simple.py
```

## Files

| File | Demonstrates |
|------|-------------|
| `move_simple.py` | Minimal async move, no hardware |
| `move_simple_led.py` | Fade an LED with `move()` |
| `move_simple_servo.py` | Move a servo with `move()` |
| `sequence_simple.py` | Async sequence, no hardware |
| `sequence_simple_servo.py` | Sequence of servo moves |
| `two_sequences_at_once.py` | Two sequences simultaneously, no hardware |
| `two_sequences_at_once_led.py` | Two LED sequences simultaneously |
| `two_sequences_at_once_servo.py` | Two servos with opposite sequences |
| `concurrent_actuators.py` | Two actuators, different speeds and easings |
| `concurrent_sequences.py` | Servo and LED each running their own sequence |
| `move_servo_and_led.py` | Servo and LED moving simultaneously |

See the sync equivalents in `examples/basic/` for comparison.

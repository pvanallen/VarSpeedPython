# CLAUDE.md

This file contains instructions for AI coding assistants working on this project.
It documents project conventions, constraints, and workflow rules.
Human contributors should also read it — it reflects the project's coding standards.

# VarSpeedPython — Async Branch (`async-rewrite`)

## Project Overview

This is the async rewrite branch of [VarSpeedPython](https://github.com/pvanallen/VarSpeedPython),
a library for generating timed, eased value sequences for actuators (servos, LEDs, etc.).
It is used in university coursework at TU Delft (Digital Interfaces course).

The library lives in the `varspeed/` package folder and is installed in editable mode
via `pip install -e .`. Always work inside the `.venv` virtual environment.

Both sync and async versions coexist:
- `varspeed/varspeed.py` — sync version (read-only). `from varspeed.varspeed import Vspeed`
- `varspeed/varspeed_async.py` — async version (canonical). `from varspeed.varspeed_async import Vspeed`
- `varspeed/easing_functions.py` — shared easing library (read-only)

---

## Constraints — Read Before Changing Anything

### Do Not Break These
- The public method names: `move()`, `sequence()`, `set_position()`, `set_bounds()`,
  `sequence_run()`, `sequence_change_seq_num()`
- Note: `move()` was intentionally removed from the async version — do not add it back
- The tuple format for sequences: `(position, time_secs, steps, easing_string[, delay_start])`
- The three-value return signature: `position, running, changed`
- The `result="int"` / `result="float"` parameter on `__init__`
- Google-style docstrings (Args/Returns/Yields sections). Every public method must have full
  docstrings — no shortcuts.

### CircuitPython Compatibility
- Target: `asyncio` via `adafruit_asyncio` (v3.x). Assume `async/await` and `asyncio.sleep()`
  are available.
- No PyPI packages. `easing_functions.py` is a local file and must remain so.
- No f-strings with format specs in CircuitPython examples (use `str()` or `%` formatting).
- Do not use async generators (async def + yield) — use `__aiter__`/`__anext__` classes
  instead. CircuitPython does not support PEP 525 async generators.
- `asyncio.create_task()` works on CircuitPython 10+ but flag it with a comment if used.
- `asyncio.Queue()` is NOT available on CircuitPython — do not use it.
- `match`/`case` (structural pattern matching) is NOT supported in CircuitPython — use `if`/`elif` instead.

### Python Version
- CPython: 3.9+
- CircuitPython: 8.x / 9.x / 10.x compatible syntax only in the core library

### Code Style
- Indentation: 2 spaces. This is a project convention inherited from the original
  codebase — not a CircuitPython requirement. Do not reformat to 4 spaces.
- No type annotations — CircuitPython does not support them in all versions.
- Two blank lines between top-level functions and classes (PEP 8).
- One blank line between methods inside a class (PEP 8).
- Constants in ALL_CAPS at module level.
- No f-strings with format specs — use `str()` or `%` formatting for CircuitPython compatibility.

---

## Code Quality Rules

### varspeed/varspeed_async.py — General Rules
- Bugs listed below have already been fixed — do not re-fix or revert them.
- Do not add new public methods without explicit instruction.
- `easing_functions` must be imported as: `from varspeed import easing_functions as ease`
  (bare `import easing_functions` will fail inside the package).

### Easing
- `easing_functions.py` is not to be modified unless explicitly instructed.
- Easing class names must be passed as strings (existing behavior). Do not refactor to pass
  class references.
- The `GammaEaseIn/Out/InOut` classes take an optional `gamma` parameter — this is not
  currently exposed in `Vspeed`. Do not expose it unless instructed.

---

## Async Conventions — Important for Beginner Pedagogy

These conventions make async code more readable for beginners. Follow them in all
examples and tutorial code.

### async for is the default — concurrency is the exception

Use `async for` as the default pattern. It is sequential and straightforward:
one move finishes, then the next begins. Only reach for `create_task()` when two
things genuinely need to run at the same time.

```python
# PREFERRED for most examples — simple, sequential, no concurrency needed
async for position, running, changed in vs.move(100, time_secs=2.0, steps=20):
    if changed:
        print(position)

# Only use create_task() when true concurrency is the point of the example
task_a = asyncio.create_task(run_actuator(vs_a, ...))
task_b = asyncio.create_task(run_actuator(vs_b, ...))
await task_a
await task_b
```

### Use create_task() instead of gather()
Prefer `asyncio.create_task()` over `asyncio.gather()` in examples. `create_task()` is
more explicit — each task is named and started individually, making it clear what is
running concurrently. `gather()` is a convenience wrapper that hides this.

```python
# PREFERRED — explicit, readable, each task is named
task_servo  = asyncio.create_task(run_actuator(vs_servo, ...))
task_led    = asyncio.create_task(run_actuator(vs_led, ...))
task_sensor = asyncio.create_task(watch_sensor(...))

await task_servo
await task_led
task_sensor.cancel()

# AVOID — hides what is running concurrently
await asyncio.gather(
    run_actuator(vs_servo, ...),
    run_actuator(vs_led, ...),
    watch_sensor(...),
)
```

### Task lifecycle — always cancel and await sleep(0)
Always cancel tasks explicitly before main() exits, and always follow with
`await asyncio.sleep(0)` to let finally blocks run:

```python
try:
    await asyncio.sleep(30)
finally:
    task_servo.cancel()
    task_sensor.cancel()
    await asyncio.sleep(0)  # lets tasks run their finally blocks
    state["pwm"].deinit()
    state["analog_in"].deinit()
```

### Hardware cleanup — use finally, not except
Use `try/finally` in tasks for hardware cleanup — it runs on normal exit,
cancellation, and exceptions. Do not use `except CancelledError` unless you need
different behavior on cancellation vs normal exit:

```python
async def run_actuator(...):
    try:
        async for position, running, changed in vs.move(...):
            ...
    finally:
        print("actuator stopped at " + str(vs.position))
```

### Shared state — use state dict and events
- Use a module-level `state` dict for continuously updated values (sensor readings,
  current positions, phase).
- Use `asyncio.Event()` for signals between tasks (threshold exceeded, timeout, done).
- Do NOT use `asyncio.Queue()` — not available on CircuitPython.
- Store hardware objects in `state` so all tasks can access them without globals:

```python
state = {}
events = {
    "sensor_high": asyncio.Event(),
    "done":        asyncio.Event(),
}

async def init():
    state["analog_in"] = analogio.AnalogIn(board.A0)
    state["pwm"]       = pwmio.PWMOut(board.D13, duty_cycle=2**15, frequency=50)
    state["servo"]     = servo.Servo(state["pwm"])
    state["servo"].angle = 0
    state["sensor_value"] = 0
    state["phase"] = "idle"
```

### Naming conventions
- `vs` — Vspeed instance
- `rs` — Rsensor instance
- `task_<noun>` — task variables: `task_servo`, `task_sensor`, `task_display`
- Helper coroutines: `run_actuator`, `run_sequence` — not `run_servo`, `run_motor`, `run_led`
- Constants: ALL_CAPS at module level

### map_range()
Use `map_range()` from the varspeed library for all sensor value conversions. Always specify
`result="int"` for servo angles, `result="float"` for brightness values:

```python
from varspeed.varspeed import map_range        # sync
from varspeed.varspeed_async import map_range  # async

angle = map_range(analog_in.value, 0, 65535, 0, 180, result="int")
```

---

## File Structure

```
varspeed/
    __init__.py             ← exposes Vspeed from varspeed.py via `from varspeed import Vspeed`
    varspeed.py             ← sync version (original). READ-ONLY.
    varspeed_async.py       ← async version (canonical). READ-WRITE.
    easing_functions.py     ← shared easing library. READ-ONLY.
rsensor.py                  ← Rsensor class and map_range utility
examples/                   ← existing sync examples. READ-ONLY. Do not touch.
examples/basic/             ← sync examples.
examples/async/             ← async examples. Already created.
README.md                   ← update to document both sync and async options
docs/easings_cheatsheet/    ← easing cheatsheet (already created)
tutorial/                   ← visual simulator app (to be created, CPython only)
pyproject.toml              ← do not modify
.venv/                      ← virtual environment, not committed to git
```

`varspeed/varspeed.py` must never be modified. If you find a bug in it,
report it in a comment — do not fix it.

Existing files in `examples/basic/` are read-only.
Do not move, rename, or reorganize them.

Library files (`easing_functions.py`, `varspeed.py`, `varspeed_async.py`) must
never be copied into the examples folders — examples import from the installed package.

---

## Examples — Rules

- Never touch any existing file in `examples/basic/`. They are read-only.
- Async examples live in `examples/async/` — already created, modify only if instructed.
- All async examples import with `from varspeed.varspeed_async import Vspeed`.
- All sync examples import with `from varspeed.varspeed import Vspeed`.
- Each async example must open with a comment block stating:
  1. What it demonstrates
  2. A one-line note pointing to the equivalent sync example
- CPython: wrap main logic in `async def main()`, call via `asyncio.run(main())`.
- CircuitPython: same `async def main()` pattern, note the entry point difference in a comment.
- The concurrent actuator and sequence examples already exist in `examples/async/` —
  do not recreate or overwrite them without explicit instruction.
- Follow the async conventions above — use `create_task()` not `gather()`.
- Pedagogical tone: beginner students. Comments explain the *why*, not just the *what*.

---

## README.md — Update Rules

- Do not restructure or remove any existing sync documentation.
- Combine sync and async documentation in a single README.md using clear callout markers.
- Any async-specific section or method must be marked with `**async only**` at the start,
  followed by the required import: `**async only** — requires \`varspeed_async.py\``
- Use the following section structure (add new sections, do not reorder existing ones):

```
## Installation
## Quick Start (sync — start here)
## Quick Start (async)
## API Reference
    ### move()        ← async only, clearly marked
    ### sequence()
    ### set_position()
    ### set_bounds()
    ### sequence_run()
    ### sequence_change_seq_num()
## Easing Functions
## Examples
    ### Sync examples
    ### Async examples
## CircuitPython Setup
## Migration: Sync → Async
```

- The "Migration: Sync → Async" section should explain the `async/await` shift clearly
  for beginners, with a before/after code comparison.
- The "Quick Start (async)" section should show the minimal working async example.
- Add a "Sync vs Async — which should I use?" callout box near the top:
  Sync = beginners, existing curriculum, CircuitPython without asyncio.
  Async = concurrent actuators, students ready to learn async patterns.
- Link to the easings cheatsheet once created.
- Do not add a second README file — one combined file only.

---

## Development Setup

The following setup is required due to a Python 3.12 / pyenv editable install issue.
Do this once after cloning the repo:

```bash
pyenv global 3.12.5
python -m venv .venv
source .venv/bin/activate
pip install -e . --config-settings editable_mode=compat
echo 'export PYTHONPATH="/Users/phil/Documents/GitHub/VarSpeedPython"' >> .venv/bin/activate
deactivate && source .venv/bin/activate
```

For each new terminal session:

```bash
source .venv/bin/activate
```

Always run examples from the repo root:

```bash
python examples/async/move_simple.py        # correct
cd examples/async && python move_simple.py  # will fail
```

Note: `.venv/` is in `.gitignore` and must not be committed. The `PYTHONPATH` line
added to `.venv/bin/activate` is machine-specific — new contributors must run the
setup sequence above on their own machine.

Add this to `pyproject.toml` to prevent Zed/ruff from reformatting 2-space indentation:

```toml
[tool.ruff]
indent-width = 2
```

---

## Git Workflow

- Branch: `async-rewrite`
- Stage all changes for review — do NOT commit automatically.
- One logical change per staged set (e.g., don't mix library fixes with example updates).
- Commit message format: `type(scope): description`
  - Types: `fix`, `feat`, `refactor`, `docs`, `chore`
  - Examples: `fix(sequence): initialize seq_loop_count in __init__`
              `docs(readme): add migration guide for async API`

---

## What Claude Code Should NOT Do Without Explicit Instruction

- Refactor `easing_functions.py`
- Add type hints or dataclasses
- Switch to a different async framework (trio, anyio)
- Add external dependencies
- Rename any public method or parameter
- Auto-commit
- Modify the university tutorial page or any external resources
- Create the tutorial app UI until the library and examples are stable and reviewed
- Add sensor-reading functionality to either library file — sensor support lives in `rsensor.py` only
- Use `asyncio.gather()` in examples — use `create_task()` instead
- Reformat indentation from 2 spaces to 4 spaces

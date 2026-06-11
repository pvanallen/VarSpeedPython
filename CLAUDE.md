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
- `varspeed/varspeed.py` — async version (canonical). `from varspeed import Vspeed`
- `varspeed/varspeed_basic.py` — sync version (read-only). `from varspeed.varspeed_basic import Vspeed`
- `varspeed/easing_functions.py` — shared easing library (read-only)

---

## Constraints — Read Before Changing Anything

### Do Not Break These
- The public method names: `move_all()`, `sequence()`, `set_position()`, `set_bounds()`,
  `sequence_run()`, `sequence_change_seq_num()`
- Note: `move()` was intentionally removed from the async version — do not add it back
- The tuple format for sequences: `(position, time_secs, steps, easing_string[, delay_start])`
- The three-value return signature: `position, running, changed`
- The `result="int"` / `result="float"` parameter on `__init__`
- Google-style docstrings (Args/Returns/Yields sections). Every public method must have full
  docstrings — no shortcuts.

### CircuitPython Compatibility
- Target: `asyncio` via `adafruit_asyncio` (v3.x). Assume `async/await` and `asyncio.sleep()`
  are available. Do NOT use `asyncio.run()` — CircuitPython uses its own entry point.
- No PyPI packages. `easing_functions.py` is a local file and must remain so.
- No f-strings with format specs in CircuitPython examples (use `str()` or `%` formatting).
- Do not use `asyncio.create_task()` without flagging it as CPython-only.

### Python Version
- CPython: 3.9+
- CircuitPython: 8.x / 9.x compatible syntax only in the core library

---

## Code Quality Rules

### varspeed/varspeed.py — General Rules
- Bugs listed below have already been fixed — do not re-fix or revert them.
- Do not add new public methods without explicit instruction.
- Indentation: 2 spaces (matches existing style).
- No type annotations — CircuitPython does not support them in all versions.
- `easing_functions` must be imported as: `from varspeed import easing_functions as ease`
  (bare `import easing_functions` will fail inside the package).

### Easing
- `easing_functions.py` is not to be modified unless explicitly instructed.
- Easing class names must be passed as strings (existing behavior). Do not refactor to pass
  class references.
- The `GammaEaseIn/Out/InOut` classes take an optional `gamma` parameter — this is not
  currently exposed in `Vspeed`. Do not expose it unless instructed.

---

## File Structure


```
varspeed/
    __init__.py             ← exposes Vspeed from varspeed.py via `from varspeed import Vspeed`
    varspeed.py             ← async version (canonical). READ-WRITE.
    varspeed_basic.py       ← sync version (original). READ-ONLY.
    easing_functions.py     ← shared easing library. READ-ONLY.
examples/                   ← existing sync examples. READ-ONLY. Do not touch.
examples/basic/             ← sync examples (moved here).
examples/async/             ← async examples. Already created.
README.md                   ← update to document both sync and async options
docs/easings_cheatsheet/    ← easing cheatsheet (already created)
tutorial/                   ← visual simulator app (to be created, CPython only)
pyproject.toml              ← do not modify
.venv/                      ← virtual environment, not committed to git```

`varspeed/varspeed_basic.py` must never be modified. If you find a bug in it,
report it in a comment — do not fix it.

Existing files in `examples/basic/` are read-only.
Do not move, rename, or reorganize them.

Library files (`easing_functions.py`, `varspeed.py`, `varspeed_basic.py`) must
never be copied into the examples folders — examples import from the installed package.

---

## Examples — Rules

- Never touch any existing file in `examples/basic/`. They are read-only.
- Async examples live in `examples/async/` — already created, modify only if instructed.
- All async examples import with `from varspeed import Vspeed`.
- All sync examples import with `from varspeed.varspeed_basic import Vspeed`.
- Each async example must open with a comment block stating:
  1. What it demonstrates
  2. A one-line note pointing to the equivalent sync example
- CPython: wrap main logic in `async def main()`, call via `asyncio.run(main())`.
- CircuitPython: same `async def main()` pattern, note the entry point difference in a comment.
- The concurrent actuator and sequence examples already exist in `examples/async/` —
  do not recreate or overwrite them without explicit instruction.
- Helper coroutines that wrap actuator motion must be named `run_actuator` or follow
  the pattern `run_<noun>` — not `run_servo`, `run_motor`, `run_led`.
- Pedagogical tone: beginner students. Comments explain the *why*, not just the *what*.

---

## README.md — Update Rules

- Do not restructure or remove any existing sync documentation.
- Combine sync and async documentation in a single README.md using clear callout markers.
- Any async-specific section or method must be marked with `**async only**` at the start,
  followed by the required import: `**async only** — requires \`varspeed.py\``
- Use the following section structure (add new sections, do not reorder existing ones):


```
## Installation
## Quick Start (sync — start here)
## Quick Start (async)
## API Reference
    ### move()
    ### move_all()        ← async only, clearly marked
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
## Migration: Sync → Async```

- The "Migration: Sync → Async" section should explain the `async/await` shift clearly
  for beginners, with a before/after code comparison.
- The "Quick Start (async)" section should show the minimal working async example.
- Add a "Sync vs Async — which should I use?" callout box near the top:
  Sync = beginners, existing curriculum, CircuitPython without asyncio.
  Async = concurrent actuators, students ready to learn async patterns.
- Link to the easings cheatsheet once created.
- Do not add a second README file — one combined file only.

## Development Setup

The following setup is required due to a Python 3.12 / pyenv editable install issue.
Do this once after cloning the repo:


```bash
pyenv global 3.12.5
python -m venv .venv
source .venv/bin/activate
pip install -e . --config-settings editable_mode=compat
echo 'export PYTHONPATH="/Users/phil/Documents/GitHub/VarSpeedPython"' >> .venv/bin/activate
deactivate && source .venv/bin/activate```

For each new terminal session:

```bash
source .venv/bin/activate```

Always run examples from the repo root:

```bash
python examples/async/move_simple.py        # correct
cd examples/async && python move_simple.py  # will fail```

Note: `.venv/` is in `.gitignore` and must not be committed. The `PYTHONPATH` line
added to `.venv/bin/activate` is machine-specific — new contributors must run the
setup sequence above on their own machine.

---



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

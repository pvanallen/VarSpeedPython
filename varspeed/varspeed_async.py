import asyncio
import time

try:
    from varspeed import easing_functions as ease
except ImportError:
    import easing_functions as ease


# Async version of Vspeed. Key differences from varspeed.py:
#
# move() replaces the sync move() poll loop. Use async for with move()
# — it steps through the entire move, yielding (position, running, changed) at
# each step. No external while loop needed.
#
# sequence() works as an async for iterator over multiple moves.
#
# Both are implemented as async iterator classes (_Move, _Sequence) rather
# than async generators, for CircuitPython compatibility — CircuitPython does
# not support PEP 525 async generators (async def + yield).
#
# Non-async methods (set_position, set_bounds, sequence_run,
# sequence_change_seq_num) are unchanged from varspeed.py.
#
# Calling patterns:
#
# # Single move
# async for pos, running, changed in vs.move(100, time_secs=2.0, steps=20):
#     print(pos)
#
# # Sequence
# async for pos, running, changed in vs.sequence(my_seq, loop_max=3):
#     print(pos)


def map_range(value, in_min, in_max, out_min, out_max, result="float"):
    """Map a value from one range to another.

    Args:
        value (int or float): input value to map.
        in_min (int or float): lower bound of the input range.
        in_max (int or float): upper bound of the input range.
        out_min (int or float): lower bound of the output range.
        out_max (int or float): upper bound of the output range.
        result (string): "int" to return a rounded integer, "float" for a float.

    Returns:
        int or float: the mapped value in the output range.
    """
    value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if result == "int":
        return round(value)
    return float(value)


class Vspeed:
    """Async version of Vspeed. Provides a non-blocking async object that generates timed value
    sequences via the move() and sequence() async iterators.
    """

    def __init__(self, init_position=0, result="int", debug=False):
        """Creates and initializes a varspeed object.

        Args:
            init_position (int/float): sets the initial position of the object.
            result (string = "int" or "float"): sets the type of the returned position.
            debug (boolean): set if varspeed will output debug info.

        Returns:
            object: returns a varspeed object
        """
        self.start_time = time.monotonic()
        self.cur_time = self.start_time
        self.started = False
        self.end_time = 0
        self.step_delay = 0
        self.increment = 0
        self.complete_range = 0.1
        self.position = init_position
        self.last_position = init_position
        self.new_position = init_position
        self.bounded = False
        self.upper_bound = 1000
        self.lower_bound = 0
        self.last_reported_position = init_position
        self.result = result
        self.step = 0
        self.increment_seq_num = True
        self.seq_pos = 0
        self.seq_run = True
        self.seq_old = []
        self.seq_loop_max = 1
        self.seq_loop_count = 0
        self.debug = debug

    def move(
        self,
        new_position=0,
        time_secs=2.0,
        steps=20,
        easing="LinearInOut",
        delay_start=0.0,
    ):
        """MOVE: Async iterator that yields all steps of a move transition.

        Preferred pattern for new code. Use in an async for loop; no external while loop needed.
        Always starts a fresh move from the current position.

        Args:
            new_position (float): new position output will change to over time_secs.
            time_secs (int): time for the transition to the new_position.
            steps (int): number of steps to change from the start position to the new_position.
            easing (string): the easing function to use for the transition.
            delay_start (float): the number of seconds to delay the start of the move.

        Yields:
            position (int or float): current position at each step.
            running (Boolean): True if more steps remain in the transition.
            changed (Boolean): True if position changed from previous step.
        """
        return _Move(self, new_position, time_secs, steps, easing, delay_start)

    def sequence(self, sequence, loop_max=1):
        """SEQUENCE: Async iterator that yields values through a sequence of moves.

        Args:
            sequence (array of tuples): moves as (position, time, steps, easing[, delay_start]).
            loop_max (int): how many times to loop the sequence; 0 loops forever.

        Yields:
            position (int or float): current position at each step.
            running (Boolean): True if more steps remain in the sequence.
            changed (Boolean): True if position changed from previous step.
        """
        return _Sequence(self, sequence, loop_max)

    def sequence_change_seq_num(self, seq_position=0):
        """Sets the current sequence number.

        Args:
            seq_position (int): jump to the element in the sequence[seq_position] array.
        """
        self.seq_pos = seq_position

    def sequence_run(self, value=True):
        """Pauses or unpauses a running sequence.

        Args:
            value (Boolean): Pauses (False) or Unpauses (True) the sequence run.
        """
        self.seq_run = value

    def set_position(self, position=0):
        """Sets the current position from which the next move will proceed.

        Args:
            position (int or float): sets the current position of the object.
        """
        self.position = position
        self.started = True

    def set_bounds(self, lower_bound=0, upper_bound=1000, bounded=True):
        """Sets the lower and upper bounds of values returned by a move or sequence.

        Args:
            lower_bound (int): sets the lower allowed bound of the output.
            upper_bound (int): sets the upper allowed bound of the output.
            bounded (Boolean): turns bounds checking on (True) or off (False).
        """
        self.bounded = bounded
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound


class _Move:
    """Async iterator for a single timed move. Returned by Vspeed.move().

    Uses __aiter__ / __anext__ rather than an async generator for CircuitPython
    compatibility (CircuitPython does not support PEP 525 async generators).
    """

    def __init__(self, vs, new_position, time_secs, steps, easing, delay_start):
        self._vs = vs
        self._new_position = new_position
        self._time_secs = time_secs
        self._steps = steps
        self._easing_name = easing
        self._delay_start = delay_start
        self._step = 0
        self._ready = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        vs = self._vs

        if not self._ready:
            vs.new_position = self._new_position
            vs.step_delay = self._time_secs / self._steps
            vs.increment = abs(vs.new_position - vs.position) / self._steps
            vs.steps = self._steps
            vs.step = 0
            vs.started = True
            easing_method = getattr(ease, self._easing_name)
            vs.ease = easing_method(
                start=vs.position, end=vs.new_position, duration=self._steps
            )
            vs.delay_start_complete = False

            if self._delay_start > 0:
                if vs.debug:
                    print("Delaying move by", self._delay_start, "secs")
                await asyncio.sleep(self._delay_start)
                vs.delay_start_complete = True

            vs.start_time = time.monotonic()
            self._ready = True

        if self._step >= self._steps:
            raise StopAsyncIteration

        await asyncio.sleep(vs.step_delay)
        self._step += 1
        vs.step = self._step
        vs.position = vs.ease(self._step)
        running = self._step < self._steps

        if not running:
            vs.position = self._new_position
            vs.started = False

        position = vs.position
        if vs.result == "int":
            position = round(vs.position)
        if vs.bounded:
            position = max(vs.lower_bound, min(position, vs.upper_bound))

        changed = vs.last_position != position
        vs.position = position
        vs.last_position = position

        if vs.debug and changed:
            print("Step %d, Position %d" % (vs.step, vs.position))

        return vs.position, running, changed


class _Sequence:
    """Async iterator over a sequence of moves. Returned by Vspeed.sequence().

    Uses __aiter__ / __anext__ rather than an async generator for CircuitPython
    compatibility.
    """

    def __init__(self, vs, sequence, loop_max):
        self._vs = vs
        self._sequence = sequence
        self._loop_max = loop_max
        self._move_iter = None

        if sequence != vs.seq_old:
            vs.seq_old = sequence
            vs.seq_pos = -1
            vs.seq_loop_count = 0
            vs.increment_seq_num = True

        vs.seq_loop_max = loop_max

    def __aiter__(self):
        return self

    async def __anext__(self):
        vs = self._vs

        while vs.seq_run:
            if self._move_iter is not None:
                try:
                    result = await self._move_iter.__anext__()
                    return result[0], True, result[2]
                except StopAsyncIteration:
                    self._move_iter = None
                    vs.increment_seq_num = True

            if vs.increment_seq_num:
                vs.seq_pos += 1
                if vs.seq_pos >= len(self._sequence):
                    if vs.seq_loop_count + 1 < self._loop_max:
                        vs.seq_pos = 0
                        vs.seq_loop_count += 1
                        if vs.debug:
                            print("LOOP", vs.seq_loop_count + 1, "of", self._loop_max)
                    elif self._loop_max == 0:
                        vs.seq_pos = 0
                        vs.seq_loop_count += 1
                        if vs.debug:
                            print("LOOP", vs.seq_loop_count + 1, "of forever")
                    else:
                        raise StopAsyncIteration
                if vs.debug:
                    print("START sequence move", vs.seq_pos, self._sequence[vs.seq_pos])
                vs.increment_seq_num = False

            step = self._sequence[vs.seq_pos]
            if len(step) < 5:
                step = step + (0.0,)

            self._move_iter = _Move(
                vs,
                new_position=step[0],
                time_secs=step[1],
                steps=step[2],
                easing=step[3],
                delay_start=step[4],
            )

        raise StopAsyncIteration


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------
async def _example():
    vs = Vspeed(init_position=0, result="int", debug=True)

    print("=== move() ===")
    vs.set_position(0)
    async for position, running, changed in vs.move(
        new_position=50, time_secs=1.0, steps=5
    ):
        print("  pos=%d, running=%s" % (position, running))

    print("=== sequence() ===")
    seq = [
        (0, 1.0, 5, "LinearInOut"),
        (100, 1.0, 5, "QuadEaseInOut"),
        (50, 1.0, 5, "LinearInOut"),
    ]
    async for position, running, changed in vs.sequence(seq, loop_max=1):
        if changed:
            print("  pos=%d" % position)


if __name__ == "__main__":
    asyncio.run(_example())

import time
import easing_functions as ease

class Vspeed():
  """Provides an non-blocking object that can be called repeatedly with the move() and sequence() functions to generate a timed series of values from a current position to a new position(s)
  """

  def __init__(self, init_position = 0, result = "int"):
    """Creates and initialzes a varspeed object.

    Args:
        init_position (int/float): sets the initial position of the object.
        result (string = "int" or "float"): sets the type of the returned position.

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
    self.easing_correction = 1
    self.result = result
    self.step = 0
    self.increment_seq_num = True
    self.seq_pos = 0
    self.seq_run = True
    self.seq_old = []
    self.seq_loop_max = 1
    self.seq_loop_count = 0

  def move(self, new_position = 0, time_secs = 2.0, steps = 20, easing = "LinearInOut"):
    """Generates a series of values that transition from the current position to a new_position

    Args:
        new_position (float): new position output will change to over time_secs
        time_secs (int): time for the transition to the new_position
        steps (int): number of steps to change from the start position to the new_position
        easing (string): the easing function to use for the transition

    Returns:
        position (int or float): each new position, marked by changed being True
        running (Boolean): if true there are more steps to go in the transition
        changed (Boolean): indicates if the latest position value is different from the previous position value

    """
    if not self.started or new_position != self.new_position:
      # print("new move")
      self.new_position = new_position
      #self.last_position = self.position
      self.start_time = time.monotonic()
      self.end_time = self.start_time + time_secs
      self.step_delay = time_secs / steps
      self.increment = abs(self.new_position - self.position) / steps
      self.steps = steps
      self.step = 0
      self.started = True
      self.easing = easing
      self.easing_method = getattr(ease, self.easing)
      self.ease = self.easing_method(start=self.position, end=self.new_position, duration=steps)

    changed = False
    running = True
    self.started = True

    #if self.new_position != self.position or self.end_time < time.monotonic():
    diff_time = time.monotonic() - self.start_time
    if diff_time > self.step_delay:
      # time to change
      self.step += 1
      # print("new step",self.step,diff_time,self.step_delay)
      self.start_time = time.monotonic()
      self.position = self.ease(self.step)
      # are we there yet?
      #if abs(new_position - self.position) < self.complete_range:
      if self.step >= self.steps:
        #force to the desired final position
        self.position = self.new_position
        running = False
        self.started = False
        # print("end of MOVE")
    else:
      changed = True

    # restrict the output to integer if needed
    if self.result == "int":
      position = round(self.position)

    # restrict the output to be within the bounds set by set_bounds()
    if self.bounded:
      position = max(self.lower_bound, min(position, self.upper_bound))

    if self.last_position == position:
        changed = False
    else:
        changed = True
    self.position = position
    self.last_position = self.position

    return self.position, running, changed

  def sequence(self, sequence, loop_max = 1):
    """Creates a series of values in a sequence of moves as specified in the sequence array

    Args:
        sequence (array of tuples): perform a sequence of moves (position,time,steps,easing) in the array
        loop_max (int): how many time to loop the sequence, zero means loop forever

    Returns:
        position (int or float): each new position, marked by changed being True
        running (Boolean): if true there are more steps to go in the transition
        changed (Boolean): indicates if the latest position value is different from the previous position value

    """
    # perform a sequence of moves in this format: (position,time,steps,easing) e.g. [(90,5,10,easing),(0,8,10,easing)]
    position = self.position
    seq_running = True
    changed = False
    self.seq_loop_max = loop_max

    if sequence != self.seq_old:
        # reset with a new sequence
        self.seq_old = sequence
        self.seq_pos = -1
        self.loop_count = 0
        self.increment_seq_num = True

    if self.seq_run: # are we running or paused?
      if self.increment_seq_num:
        self.seq_pos += 1
        if self.seq_pos >= len(sequence):
          if self.loop_count + 1 < self.seq_loop_max:
              self.seq_pos = 0
              self.loop_count += 1
              print("LOOP",self.loop_count + 1,"of",self.seq_loop_max)
          elif self.seq_loop_max == 0: # loop forever
              self.seq_pos = 0
              self.loop_count += 1
              print("LOOP",self.loop_count + 1,"of forever")
          else:
            return position, False, False
        print("START sequence move",self.seq_pos,sequence[self.seq_pos])
        self.increment_seq_num = False

      position, running, changed = self.move(
        new_position=sequence[self.seq_pos][0],
        time_secs=sequence[self.seq_pos][1],
        steps=sequence[self.seq_pos][2],
        easing=sequence[self.seq_pos][3])

      if not running: # finished with move
        self.increment_seq_num = True
        # print("FINISHED sequence move",self.seq_pos)
      if changed:
        return position,True,True

        # go to the next move in sequence

    else: # we're paused and exit
      seq_running = False

    return position, seq_running, False

  def sequence_change_seq_num(self, seq_position = 0):
    """Sets the current sequence number

    Args:
        seq_position (int): jump to the element in the sequence[seq_position] array

    Returns:
        nothing

    """
    self.seq_pos = seq_position

  def sequence_run(self, value = True):
    """Pauses or Unpauses a running sequence

    Args:
        value (Boolean): Pauses (False) or Unpauses (True) the run of the sequence

    Returns:
        nothing

    """
    self.seq_run = value

  def set_position(self, position = 0):
    """Sets the current position from which the next move will proceed

    Args:
        position (int or float): sets the current position of the object

    Returns:
        nothing

    """
    self.position = position
    self.started = True

  def set_bounds(self, lower_bound = 0, upper_bound = 1000, bounded=True):
    """Sets the lower and upper bounds of values returned by a move or sequence

    Args:
        lower_bound (int): sets the lower allowed bound of the output of a move or sequnce
        upper_bound (int): sets the upper allowed bound of the output of a move or sequnce
        bounded (Boolean): turns bounds checking on (True - Default) or off (False)

    Returns:
        nothing

    """
    self.bounded = bounded
    self.upper_bound = upper_bound
    self.lower_bound = lower_bound

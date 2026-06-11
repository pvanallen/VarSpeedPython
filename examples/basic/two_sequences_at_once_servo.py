# two_sequences_at_once_servo.py
#
# an example of how to use two sequences at the same time without blocking either one
#
import board
import pwmio
from adafruit_motor import servo
from varspeed import Vspeed

MIN = 15
MAX = 165

# create a PWMOut object on Pin D13
pwm1 = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
# create a PWMOut object on Pin D4
pwm2 = pwmio.PWMOut(board.D4, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo1 = servo.Servo(pwm1)
my_servo2 = servo.Servo(pwm2)

# set up the varspeed objects
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info
vs1 = Vspeed(init_position=MIN, result="int", debug=False)
# make the output of the function be within the bounds set
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)
vs2 = Vspeed(init_position=MAX, result="int", debug=False)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)

# set the servo to a known starting point
my_servo1.angle = vs1.position
my_servo2.angle = vs2.position

my_sequence1 = [(MIN, 1, 100, "QuadEaseIn",2),
                (MAX, 1, 100, "QuadEaseIn",2)]

my_sequence2 = [(MAX, 1, 100, "QuadEaseIn",2),
                (MIN, 1, 100, "QuadEaseIn",2)]

running1 = True
running2 = True
#print("starting  position",vs.position)
while running1 and running2:
  # run a sequence of moves
  # sequence(sequence,loop,loop_max)
  # sequence = moves in this format: (next-position,secs-to-move,number-of-steps,easing function,delay_start)
  #     example: [(90,5,10,LinearInOut,2),(0,8,10,QuadEaseInOut,2),(180,5,10,CubicEaseIn,2)]
  # loop_max = number of times to run the sequence in a loop
  #     if zero, loop forever
  #     if 1, play once
  #     if >1, loop sequence that many times
  #
    position1, running1, changed1 = vs1.sequence(
        sequence=my_sequence1, loop_max=3)
    if changed1:
        #print(
        #    f'Sequence Num: {vs1.seq_pos}, Step: {vs1.step}, Position: {position1}')
        my_servo1.angle = position1

    position2, running2, changed2 = vs2.sequence(
        sequence=my_sequence2, loop_max=3)
    if changed2:
        #print(
        #    f'Sequence Num: {vs2.seq_pos}, Step: {vs2.step}, Position: {position2}')
        my_servo2.angle = position2

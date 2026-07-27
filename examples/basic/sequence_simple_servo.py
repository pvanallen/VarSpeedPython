# sequence_simple_servo.py
#
# an example of using the VarSpeedPython class to have a series of moves in a sequence
#
import time
import board
import pwmio
from adafruit_motor import servo
from varspeed import Vspeed

MIN = 0
MAX = 180

# set up the varspeed object
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info
vs = Vspeed(init_position=MIN, result="int", debug=True)
# make the output of the function be within the bounds set
vs.set_bounds(lower_bound=MIN, upper_bound=MAX)

# create a PWMOut object on Pin D13.
pwm = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

# set the servo to a known starting point
my_servo.angle = MIN

# note that these sequence moves may include a last delay_start parameter 
my_sequence = [(MAX, 2.0, 100, "QuadEaseIn"), # missing delay_start parameter defaults to 0.0
               (MIN, 2.0, 100, "QuadEaseOut",3), # waits 3 seconds to start
               (MAX, 2.0, 100, "SineEaseInOut",2), # waits 2 seconds to start
               ] 

running = True
while running:
    # run a sequence of moves
    # sequence(sequence,loop,loop_max)
    #     sequence = moves in this format: (next-position,secs-to-move,number-of-steps,easing function)
    #       example: [(90,5,10,LinearInOut),(0,8,10,QuadEaseInOut),(180,5,10,CubicEaseIn)]
    #     loop_max = number of times to run the sequence in a loop
    #         if zero, loop forever
    #         if 1, play once
    #         if >1, loop sequence that many times
    #
    position, running, changed = vs.sequence(sequence=my_sequence, loop_max=1)

    if changed:
        my_servo.angle = position

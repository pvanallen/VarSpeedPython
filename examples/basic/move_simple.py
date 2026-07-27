# move_simple.py
#
# a non-hardware dependent example of using the VarSpeedPython class
# to ramp a value from one level to another
#
from varspeed import Vspeed

MIN = 0
MAX = 100

# set up the varspeed object
#
# init_position = initial start position
# result = float, int
# debug = False, True # set if varspeed will output debug info

vs = Vspeed(init_position=MIN, result="int", debug=False)

running = True
while running:
    # move from the current position
    # move(new_position,time_secs of move,steps in move,easing function)
    # for more into on easing, see: https://github.com/semitable/easing-functions
    # for a visual repesentation of the easing options see:
    #     http://www.emix8.org/forum/viewtopic.php?t=1063
    position, running, changed = vs.move(
        new_position=MAX, time_secs=0.5, steps=10, easing="LinearInOut")
    if changed:
        print(f'Step: {vs.step}, Position: {position}')

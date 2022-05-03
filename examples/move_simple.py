import time

from varspeed import Vspeed

MIN = 0
MAX = 180

# set up the varspeed object
#
# init_position = initial start position
# result = float, int
vs = Vspeed(init_position=MAX, result="int")

running = True
while running:
    # move from the current position
    # move(new_position,time_secs of move,steps in move,easing function)
    # for more into on easing, see: https://github.com/semitable/easing-functions
    # for a visual repesentation of the easing options see:
    #     http://www.emix8.org/forum/viewtopic.php?t=1063
    position, running, changed = vs.move(
        new_position=MIN, time_secs=0.5, steps=9, easing="LinearInOut")
    if changed:
        print(f'Step: {vs.step}, Position: {position}')

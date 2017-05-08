#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

#Go in a straight line
btn = ev3.Button() # will use any button to stop script
#Init motors
mR = ev3.LargeMotor('outA')
mL = ev3.LargeMotor('outD')
#Reset motors
mR.reset()
mL.reset()
while not btn.any():
        mR.run_forever(speed_sp=450)
        mL.run_forever(speed_sp=450)
        print("L/Rencoders: %d | %d" % (mL.position, mR.position))
        sleep(0.1)

mR.stop(stop_action='brake')
mL.stop(stop_action='brake')

#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
mR = ev3.LargeMotor('outA')
mL = ev3.LargeMotor('outD')
mR.stop(stop_action='brake')
mL.stop(stop_action='brake')

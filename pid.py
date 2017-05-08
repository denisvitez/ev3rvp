#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

#Go in a straight line
#Left motor will be MASTER --> mL
btn = ev3.Button() # will use any button to stop script
#Init motors
mR = ev3.LargeMotor('outA')
mL = ev3.LargeMotor('outD')
#Reset motors
mR.reset()
mL.reset()
#Init PID parameters
errorPrior = 0
integral = 0
kP = 2
kI = 20
kD = 1
iterTime = 0.1
bias = 0
while not btn.any():
        error = mL.position - mR.position
        print("Error is: %d", (error))
        integral = integral + (error * iterTime)
        derivative = (error - errorPrior) / iterTime
        output = kP*error + kI*integral + kD*derivative + bias
        print("Output is: %d", (output))
        mR.run_forever(speed_sp=450+output)
        mL.run_forever(speed_sp=450)
        print("L/Rencoders: %d | %d" % (mL.position, mR.position))
        sleep(iterTime)

mR.stop(stop_action='brake')
mL.stop(stop_action='brake')

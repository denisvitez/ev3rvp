#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

#Go in a straight line
#Left motor will be MASTER --> mL
btn = ev3.Button() # will use any button to stop script
#Init motors
mR = ev3.LargeMotor('outA')
mL = ev3.LargeMotor('outD')
maxR = mR.max_speed
maxL = mL.max_speed
targetSpeed = 450
#Reset motors
mR.reset()
mL.reset()
#Init PID parameters --> tuned with Ziegler–Nichols method
errorPrior = 0.0
integral = 0.0
kP = 5.4
kI = 21.6
kD = 0.33
iterTime = 0.1
bias = 0
#Some statistics
sumError = 0
#main loop
while not btn.any():
        error = mL.position - mR.position
        sumError += error
        print("Error is: %d", (error))
        integral = integral + (error * iterTime)
        derivative = (error - errorPrior) / iterTime
        output = kP*error + kI*integral + kD*derivative + bias
        print("Output is: %d", (output))
        actualSpeed = targetSpeed + output
        if(actualSpeed < 0):
            actualSpeed = 0
        if(actualSpeed > maxR):
            actualSpeed = maxR
        mR.run_forever(speed_sp=actualSpeed)
        mL.run_forever(speed_sp=targetSpeed)
        print("L/Rencoders: %d | %d --> difference in encoded steps is %d" % (mL.position, mR.position, error))
        sleep(iterTime)
#stop motors
mR.stop(stop_action='brake')
mL.stop(stop_action='brake')
#output statistics
print("Finished running the programm.")
print("The sum of all errors is: %d" % (sumError))

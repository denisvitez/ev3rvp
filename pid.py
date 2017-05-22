#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
import paho.mqtt.client as mqtt
from threading import Thread
from multiprocessing import Process

# Go in a straight line
# Left motor will be MASTER --> mL
btn = ev3.Button() # will use any button to stop script
client = mqtt.Client()
client.connect("vitez.si", 1883, 60)
# Init motors
mR = ev3.LargeMotor('outA')
mL = ev3.LargeMotor('outD')
maxR = mR.max_speed
maxL = mL.max_speed
targetSpeed = 450
# Init light sensor
cl = ev3.ColorSensor()
cl.mode='COL-REFLECT'
blackValue = 15
#Init gyro
gy = ev3.GyroSensor()
# Gyro can be reset with changing between modes :) (WTF!)
gy.mode = 'GYRO-ANG'
gy.mode = 'GYRO-RATE'
gy.mode='GYRO-ANG'
# Init PID parameters --> tuned with Ziegler–Nichols method

kP = 3.6
kI = 18
kD = 0.18
iterTime = 0.05
bias = 0
masterKoeficient = 0.99
#masterKoeficient = 0.999
#Some statistics
sumError = 0
sumPositiveError = 0
sumNegativeError = 0


def stop():
    # stop motors
    mR.stop(stop_action='brake')
    mL.stop(stop_action='brake')


def goStraight(blackWait, skipLines):
    # main loop
    # Reset motors
    waitStarted = False
    iterationsWaited = 0
    mR.reset()
    mL.reset()
    try:
        while not btn.any():
            if(cl.value() < blackValue and not waitStarted):
                waitStarted = True
            if waitStarted:
                iterationsWaited += 1
                if iterationsWaited > blackWait:
                    if skipLines <= 0:
                        return
                    else:
                        skipLines -= 1
                        iterationsWaited = 0
                        waitStarted = False
            global sumError
            global sumPositiveError
            global sumNegativeError
            errorPrior = 0.0
            integral = 0.0
            error = (mL.position * masterKoeficient) - mR.position
            sumError += error
            if(error > 0):
                sumPositiveError += error
            else:
                sumNegativeError += error * -1
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
            client.publish("ev3/speed", actualSpeed)
            sleep(iterTime)
    except KeyboardInterrupt:
        pass


def rotate(target, rotationSpeed):
    while True:
        angle = gy.value()
        if(angle == target):
            return
        diff = angle - target
        print("Angle diff is: "+str(diff))
        targetSpeed = diff * 5
        if diff > 0:
            targetSpeed += 10
        if diff < 0:
            targetSpeed -= 10
        if(targetSpeed > 0 and targetSpeed > rotationSpeed):
            targetSpeed = rotationSpeed
        if(targetSpeed < 0 and targetSpeed < -rotationSpeed):
            targetSpeed = -rotationSpeed
        print("Target speed is: "+str(targetSpeed))
        mR.run_forever(speed_sp=-targetSpeed)
        mL.run_forever(speed_sp=+targetSpeed)
        sleep(0.1)


def readColor():
    try:
        while True:
            print("IR loop")
            print(cl.value())
            sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    goStraight(10, 1)
    stop()
    rotate(180, 100)
    stop()
    goStraight(10, 1)
    rotate(0, 100)
    stop()
    goStraight(10, 2)
    stop()
    rotate(180, 100)
    stop()
    goStraight(10, 2)
    rotate(0, 100)
    stop()
    goStraight(10, 3)
    stop()
    rotate(180, 100)
    stop()
    goStraight(10, 3)
    rotate(0, 100)
    stop()
    # output statistics
    print("Finished running the programm.")
    print("The sum of all errors is: %d" % (sumError))
    print("The sum of positive errors is: %d" % (sumPositiveError))
    print("The sum of negative errors is: %d" % (sumNegativeError))

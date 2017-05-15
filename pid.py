#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
import paho.mqtt.client as mqtt
from threading import Thread
from multiprocessing import Process

#Go in a straight line
#Left motor will be MASTER --> mL
btn = ev3.Button() # will use any button to stop script
client = mqtt.Client()
client.connect("vitez.si", 1883, 60)
#Init motors
mR = ev3.LargeMotor('outA')
mL = ev3.LargeMotor('outD')
maxR = mR.max_speed
maxL = mL.max_speed
targetSpeed = 450
#Init light sensor
cl = ev3.ColorSensor()
cl.mode='COL-REFLECT'
blackValue = 10
#Init gyro
gy = ev3.GyroSensor()
#Gyro can be reset with changing between modes :) (WTF!)
gy.mode = 'GYRO-ANG'
gy.mode = 'GYRO-RATE'
gy.mode='GYRO-ANG'
#Init PID parameters --> tuned with Ziegler–Nichols method

kP = 6
kI = 30
kD = 0.3
iterTime = 0.05
bias = 0
masterKoeficient = 1
#masterKoeficient = 0.999
#Some statistics
sumError = 0
sumPositiveError = 0
sumNegativeError = 0
def stop():
    #stop motors
    mR.stop(stop_action='brake')
    mL.stop(stop_action='brake')
def goStraight(blackWait, skipLines):
    #main loop
    #Reset motors
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
            error = (mL.position*masterKoeficient) - mR.position
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
            #client.publish("ev3/speed", actualSpeed);
            if(actualSpeed < 0):
                actualSpeed = 0
            if(actualSpeed > maxR):
                actualSpeed = maxR
            mR.run_forever(speed_sp=actualSpeed)
            mL.run_forever(speed_sp=targetSpeed)
            print("L/Rencoders: %d | %d --> difference in encoded steps is %d" % (mL.position, mR.position, error))
            sleep(iterTime)
    except KeyboardInterrupt:
        pass

def rotate(target, rotationSpeed):
    while True:
        angle = gy.value()
        if(angle == target):
            return
        if(angle < target):
            mR.run_forever(speed_sp=rotationSpeed)
            mL.run_forever(speed_sp=-rotationSpeed)
        elif(angle > target):
            mR.run_forever(speed_sp=-rotationSpeed)
            mL.run_forever(speed_sp=rotationSpeed)
        sleep(0.05)

def readColor():
    try:
        while True:
            print("IR loop")
            print(cl.value())
            sleep(0.1)
    except KeyboardInterrupt:
        pass


#Main code
goStraight(10, 1)
stop()
rotate(180, 200)
stop()
goStraight(10, 1)
rotate(0, 200)
stop()
goStraight(10, 2)
stop()
rotate(180, 200)
stop()
goStraight(10, 2)
rotate(0, 200)
stop()
#output statistics
print("Finished running the programm.")
print("The sum of all errors is: %d" % (sumError))
print("The sum of positive errors is: %d" % (sumPositiveError))
print("The sum of negative errors is: %d" % (sumNegativeError))

#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
btn = ev3.Button()
gy = ev3.GyroSensor()
#Gyro can be reset with changing between modes :) (WTF!)
gy.mode = 'GYRO-ANG'
gy.mode = 'GYRO-RATE'
gy.mode='GYRO-ANG'
while not btn.any():
    print("Gyro loop")
    angle = gy.value()
    print(str(angle))
    sleep(0.1)

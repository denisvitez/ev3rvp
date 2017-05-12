#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
btn = ev3.Button()
cl = ev3.ColorSensor()
cl.mode='COL-REFLECT'
while not btn.any():
    print("IR loop")
    print(cl.value())
    sleep(0.1)

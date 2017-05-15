#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("vitez.si", 1883, 60)
client.publish("ev3/test", "Hello world!");
client.disconnect();

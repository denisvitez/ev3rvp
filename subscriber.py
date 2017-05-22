import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt

plt.ion()
x_data = []
y_data = []
y = 0

def on_connect(client, userdata, rc):
    client.subscribe("ev3/speed")
    print("Subscribed to topic EV3")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.payload)
    global x
    global y
    global x_data
    y += 1
    y_data.append(y)
    x_data.append(msg.payload)
    plt.plot(y_data, x_data)
    plt.show()
    plt.pause(0.0001)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("vitez.si", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

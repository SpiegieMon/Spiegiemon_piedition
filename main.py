#!/usr/bin/python3
import sx126x
import os
from threading import Thread, Lock

ttydevices = ["/dev/ttyS0", "/dev/ttyAMA0"]

if os.path.exists(ttydevices[0]):
    ttydevice = ttydevices[0]
else:
    ttydevice = ttydevices[1]
node = sx126x.sx126x(serial_num = ttydevice, freq=868, addr=100, power=22, rssi=True)

node_lock = Lock()


def send(data):
    with node_lock:
        node.send(data)


def input_loop():
    text = input()
    send(text)


input_thread = Thread(target=input_loop)
input_thread.start()

while True:
    with node_lock:
        node.receive()
input_thread.exit()

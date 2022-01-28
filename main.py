#!/usr/bin/python3
import sx126x
import os
from threading import Thread, Lock

def get_serial_tty():
    choices = ["/dev/ttyS0", "/dev/ttyAMA0"]
    for device in choices:
        if os.path.exists(device):
            return device

node = sx126x.sx126x(serial_num=get_serial_tty(), freq=868, addr=100, power=22, rssi=True)

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

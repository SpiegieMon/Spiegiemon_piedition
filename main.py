#!/usr/bin/python3
import sx126x
import os
from threading import Thread, Lock
import pyprctl

pyprctl.set_name("main")


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
    pyprctl.set_name("input_loop")
    while True:
        text = input()
        if text == 'q':
            break
        send(text)


input_thread = Thread(target=input_loop)
input_thread.start()

while input_thread.is_alive():
    with node_lock:
        node.receive()

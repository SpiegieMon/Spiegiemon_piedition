#!/usr/bin/python3
import bttr_sx126x
import os
import sys
import signal
from threading import Thread, Lock

ttydevices = ["/dev/ttyS0", "/dev/ttyAMA0"]

if os.path.exists(ttydevices[0]):
    ttydevice = ttydevices[0]
else:
    ttydevice = ttydevices[1]
node = bttr_sx126x.sx126x(serial_num = ttydevice,freq=868,addr=100,power=22,rssi=True)

node_lock = Lock()

def send(data):
    node_lock.acquire()
    node.send(data)
    node_lock.release()

def input_loop():
    text = input()
    send(text)

input_thread = Thread(target=input_loop)
input_thread.start()

while True:
    node_lock.acquire()
    node.receive()
    node_lock.release()
input_thread.exit()

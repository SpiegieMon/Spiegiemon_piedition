#!/usr/bin/python3
from console_input import ConsoleInput
from reciever import Receiver
from sender import Sender
from sx126x import sx126x
import os
from threading import Lock
import pyprctl
from queue import Queue

pyprctl.set_name("main")


def get_serial_tty():
    choices = ["/dev/ttyS0", "/dev/ttyAMA0"]
    for device in choices:
        if os.path.exists(device):
            return device


if __name__ == "__main__":
    node = sx126x(serial_num=get_serial_tty(), freq=868, addr=100, power=22, rssi=True)

    data_queue = Queue()
    node_lock = Lock()

    console_input_thread = ConsoleInput(data_queue)
    console_input_thread.start()

    sender_thread = Sender(node, node_lock, data_queue)
    sender_thread.start()

    receive_thread = Receiver(node, node_lock)
    receive_thread.start()
    
    try:
        console_input_thread.join()
    except KeyboardInterrupt:
        print("exiting by keyboard interrupt")


    print("Programm exited gracefully")

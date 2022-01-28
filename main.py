#!/usr/bin/python3
import sx126x
import os
from threading import Thread, Lock
import pyprctl
import select
from queue import Queue

pyprctl.set_name("main")

class Receiver(Thread):
    def __init__(self, node, lock):
        Thread.__init__(self, daemon=True)
        self.setName("receiver")
        self.node = node
        self.lock = lock

    def run(self):
        while True:
            select.select([self.node.ser], [], [self.node.ser])
            with self.lock:
                self.node.receive()

class Inputer(Thread):
    def __init__(self, queue):
        Thread.__init__(self, daemon=True)
        self.queue = queue

    def add_queue(self, message):
        self.queue.put(message)

    def run(self):
        while True:
            text = input("input: ")
            if text == 'q':
                break
            self.add_queue(text)

class Sender(Thread):
    def __init__(self, node, lock, queue):
        Thread.__init__(self, daemon=True)
        self.setName("receiver")
        self.node = node
        self.lock = lock
        self.queue = queue

    def send(self, data):
        with node_lock:
            node.send(data)
    
    def run(self):
        while True:
            message = self.queue.get()
            self.send(message)



def get_serial_tty():
    choices = ["/dev/ttyS0", "/dev/ttyAMA0"]
    for device in choices:
        if os.path.exists(device):
            return device


if __name__ == "__main__":
    node = sx126x.sx126x(serial_num=get_serial_tty(), freq=868, addr=100, power=22, rssi=True)

    data_queue = Queue()
    node_lock = Lock()

    inputer_thread = Inputer(data_queue)
    inputer_thread.start()

    sender_thread = Sender(node, node_lock, data_queue)
    sender_thread.start()

    receive_thread = Receiver(node, node_lock)
    receive_thread.start()
    
    try:
        inputer_thread.join()
    except KeyboardInterrupt:
        print("exiting by keyboard interrupt")


    print("Programm exited gracefully")

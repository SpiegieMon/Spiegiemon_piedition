#!/usr/bin/python3
import sx126x
import os
from threading import Thread, Lock, Event
import pyprctl

pyprctl.set_name("main")

class Receiver(Thread):
    def __init__(self, node, lock, event):
        Thread.__init__(self)
        self.running = True
        self.node = node
        self.lock = lock
        self.quit_event = event

    def run(self):
        while not self.quit_event.is_set(): 
            with self.lock:
                self.node.receive()



class Sender(Thread):
    def __init__(self, node, lock, event):
        Thread.__init__(self)
        self.running = True
        self.node = node
        self.lock = lock
        self.quit_event = event

    def send(self,data):
        with node_lock:
            node.send(data)
    
    def run(self):
        while not self.quit_event.is_set():
            text = input("input: ")
            if text == 'q':
                break
            self.send(text)


def get_serial_tty():
    choices = ["/dev/ttyS0", "/dev/ttyAMA0"]
    for device in choices:
        if os.path.exists(device):
            return device

node = sx126x.sx126x(serial_num=get_serial_tty(), freq=868, addr=100, power=22, rssi=True)

node_lock = Lock()


quit_event = Event()

sender_thread = Sender(node, node_lock, quit_event)
sender_thread.start()

receive_thread = Receiver(node, node_lock, quit_event)
receive_thread.start()

sender_thread.join()
receive_thread.join()

print("Programm exited gracefully")

## while input_thread.is_alive():
##     with node_lock:
##         node.receive()

#!/usr/bin/python3
from console_input import ConsoleInput
from reciever import Receiver
from sender import Sender
from sx126x import sx126x
import os
from threading import Lock, Thread
import pyprctl
from queue import Queue
from serial import Serial, SerialException
import select
import inotify.adapters
import inotify.constants
import time

pyprctl.set_name("main")


class Bluetooth_input(Thread):
    def __init__(self, lock: Lock, input_queue: Queue, output_queue: Queue):
        Thread.__init__(self, daemon=True)
        self.lock = lock
        self.input_queue = input_queue
        self.inotify_adapter = inotify.adapters.Inotify()
        self.dev_dir = '/dev'
        self.rfcomm = 'rfcomm0'
        self.inotify_adapter.add_watch(self.dev_dir, mask=inotify.constants.IN_CREATE)

    def run(self):
        while True:
            if os.path.exists('/dev/rfcomm0'):
                try:
                    ser = Serial('/dev/rfcomm0')
                    while ser.isOpen():
                        select.select([ser], [], [ser])
                        data = ser.readline()
                        data = data[:-2].decode('utf-8')
                        print(data)
                        self.input_queue.put(data)
                except SerialException:
                    ser.close()
                    print("BTdevice disconnected")

            else:
                print("listening for incoming connection")
                for event in self.inotify_adapter.event_gen(yield_nones=False):
                    (_, type_names, path, filename) = event
                    if filename == self.rfcomm:
                        time.sleep(1)
                        print("device connected")
                        break




def get_serial_tty():
    choices = ["/dev/ttyS0", "/dev/ttyAMA0"]
    for device in choices:
        if os.path.exists(device):
            return device


if __name__ == "__main__":
    node = sx126x(serial_num=get_serial_tty(), freq=868, addr=100, power=22, rssi=True)

    data_queue = Queue()
    output_queue = Queue()
    node_lock = Lock()

    bluetooth_input_thread = Bluetooth_input(node_lock, data_queue, output_queue)
    bluetooth_input_thread.start()

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

#!/usr/bin/env python3
# This file is part of SpiegieMon. https://github.com/SpiegieMon/Spiegiemon_piedition/
# (C) 2022 Michael Spiegelhalter <michael.spi@web.de>

import sys
import time
from queue import Queue
from threading import Lock

import pyprctl

import sx126x
from bluetooth_queue_adapter import BluetoothQueueAdapter
from console_input import ConsoleInput
from lora_receiver import LoraReceiver
from lora_sender import LoraSender
from sx126x import Sx126x

pyprctl.set_name("main")


if __name__ == "__main__":
    node = Sx126x(serial_num=sx126x.get_serial_tty(), freq=868, addr=100, power=22, rssi=True)

    lora_send_queue = Queue()
    bluetooth_send_queue = Queue()
    node_lock = Lock()

    bluetooth_thread = BluetoothQueueAdapter(lora_send_queue, bluetooth_send_queue)
    bluetooth_thread.start()

    sender_thread = LoraSender(node, node_lock, lora_send_queue)
    sender_thread.start()

    receive_thread = LoraReceiver(node, node_lock, bluetooth_send_queue)
    receive_thread.start()

    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        console_input_thread = ConsoleInput(lora_send_queue)
        console_input_thread.start()

        try:
            console_input_thread.join()
        except KeyboardInterrupt:
            print("exiting by keyboard interrupt")
    else:
        while True:
            time.sleep(10000)

    print("Programm exited gracefully")

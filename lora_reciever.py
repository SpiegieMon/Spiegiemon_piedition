#!/usr/bin/env python3
# This file is part of SpiegieMon. https://github.com/Spiegie/Spiegiemon_piedition/
# (C) 2022 Michael Spiegelhalter <michael.spi@web.de>
import select
from queue import Queue
from threading import Thread, Lock

from sx126x import sx126x


class LoraReceiver(Thread):
    def __init__(self, node: sx126x, lock: Lock, queue: Queue):
        Thread.__init__(self, daemon=True)
        self.setName("LoraReceiver")
        self.node = node
        self.lock = lock
        self.output_queue = queue

    def run(self):
        while True:
            select.select([self.node.ser], [], [self.node.ser])
            with self.lock:
                rssi, node, data = self.node.receive()
                print(f"\nRecieved '{data.decode()}' from {node}")
                self.output_queue.put(data.decode())
                print('input: ', end='')

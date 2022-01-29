#!/usr/bin/env python3
# This file is part of SpiegieMon. https://github.com/Spiegie/Spiegiemon_piedition/
# (C) 2022 Michael Spiegelhalter <michael.spi@web.de>
import time
from queue import Queue
from threading import Thread, Lock

from sx126x import sx126x


class LoraSender(Thread):
    def __init__(self, node: sx126x, lock: Lock, queue: Queue):
        Thread.__init__(self, daemon=True)
        self.setName("LoraSender")
        self.node = node
        self.lock = lock
        self.queue = queue

    def send(self, data: str):
        with self.lock:
            self.node.send(data)

    def run(self):
        while True:
            message = self.queue.get()
            self.send(message)
            time.sleep(1)

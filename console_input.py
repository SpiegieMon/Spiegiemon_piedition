#!/usr/bin/env python3
# This file is part of SpiegieMon. https://github.com/SpiegieMon/Spiegiemon_piedition/
# (C) 2022 Michael Spiegelhalter <michael.spi@web.de>
from queue import Queue
from threading import Thread


class ConsoleInput(Thread):
    def __init__(self, queue: Queue):
        Thread.__init__(self, daemon=True)
        self.queue = queue
        self.setName("ConsoleInput")

    def add_queue(self, message: str):
        self.queue.put(message)

    def run(self):
        while True:
            text = input("input: ")
            if text == 'q':
                break
            if len(text) == 0:
                continue
            self.add_queue(text)

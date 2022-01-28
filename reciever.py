import select
import sys
from threading import Thread, Lock

from sx126x import sx126x


class Receiver(Thread):
    def __init__(self, node: sx126x, lock: Lock):
        Thread.__init__(self, daemon=True)
        self.setName("receiver")
        self.node = node
        self.lock = lock

    def run(self):
        while True:
            select.select([self.node.ser], [], [self.node.ser])
            with self.lock:
                rssi, node, data = self.node.receive()
                print(f"\nRecieved '{data.decode()}' from {node}")

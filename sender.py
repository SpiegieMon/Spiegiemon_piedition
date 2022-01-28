from queue import Queue
from threading import Thread, Lock

from main import node_lock, node
from sx126x import sx126x


class Sender(Thread):
    def __init__(self, node: sx126x, lock: Lock, queue: Queue):
        Thread.__init__(self, daemon=True)
        self.setName("receiver")
        self.node = node
        self.lock = lock
        self.queue = queue

    def send(self, data: str):
        with node_lock:
            node.send(data)

    def run(self):
        while True:
            message = self.queue.get()
            self.send(message)
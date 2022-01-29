#!/usr/bin/python3
from bluetooth import BluetoothSocket

from console_input import ConsoleInput
from reciever import Receiver
from sender import Sender
from sx126x import sx126x
import os
from threading import Lock, Thread
import pyprctl
from queue import Queue
import bluetooth

pyprctl.set_name("main")


class Bluetooth_input(Thread):
    def __init__(self, input_queue: Queue, output_queue: Queue):
        Thread.__init__(self, daemon=True)
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.server = BluetoothSocket(bluetooth.RFCOMM)
        self.server.bind(("", bluetooth.PORT_ANY))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        self.service_id = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    def run(self):
        bluetooth.advertise_service(self.server, "SampleServer", service_id=self.service_id,
                                    service_classes=[self.service_id, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Waiting for conn on rfcomm chan", self.port)
        while True:
            client_sock, client_info = self.server.accept()
            print("Accepted connection from", client_info)
            bluetooth_sender = BluetoothSender(client_sock, self.output_queue)
            bluetooth_sender.start()
            try:
                while True:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    data_str = data.decode("UTF-8").strip("\n")
                    print("Recieved:", data_str)
                    self.input_queue.put(data_str)
            except OSError:
                pass
            print("Bluetooth client disconnected")
            client_sock.close()
            print("Waiting for bluetooth sender thread to exit")
            bluetooth_sender.join(timeout=10)
            if bluetooth_sender.is_alive():
                print("Timed out waiting for bluetooth sender thread")
            print("Waiting for new connection on rfcomm chan", self.port)


class BluetoothSender(Thread):
    def __init__(self, client_socket: BluetoothSocket, lora_input: Queue):
        Thread.__init__(self, daemon=True)
        self.client_socket = client_socket
        self.stop_running = False
        self.lora_input = lora_input

    def run(self):
        print(vars(self.client_socket))
        while self.client_socket.connected:
            data = self.lora_input.get()
            try:
                self.client_socket.send(data)
            except OSError as e:
                if self.client_socket.connected:
                    print("Unexpected error:")
                    print(e)
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

    bluetooth_input_thread = Bluetooth_input(data_queue, output_queue)
    bluetooth_input_thread.start()

    console_input_thread = ConsoleInput(data_queue)
    console_input_thread.start()

    sender_thread = Sender(node, node_lock, data_queue)
    sender_thread.start()

    receive_thread = Receiver(node, node_lock, output_queue)
    receive_thread.start()

    try:
        console_input_thread.join()
    except KeyboardInterrupt:
        print("exiting by keyboard interrupt")

    print("Programm exited gracefully")

#!/usr/bin/env python3
# This file is part of SpiegieMon. https://github.com/Spiegie/Spiegiemon_piedition/
# (C) 2022 Michael Spiegelhalter <michael.spi@web.de>
import queue
import sys
from queue import Queue
from threading import Thread

import bluetooth
from bluetooth import BluetoothSocket


class BluetoothQueueAdapter(Thread):
    def __init__(self, input_queue: Queue, output_queue: Queue):
        Thread.__init__(self, daemon=True)
        self.setName("BluetoothQueueAdapter")
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
                    client_sock.send("Received: " + data_str + "\n")
                    self.input_queue.put(data_str)
            except OSError:
                pass
            print("Bluetooth client disconnected")
            client_sock.close()
            bluetooth_sender.stop_running = True
            bluetooth_sender.join(timeout=10)
            if bluetooth_sender.is_alive():
                print("Timed out waiting for bluetooth sender thread", file=sys.stderr)
            print("Waiting for new connection on rfcomm chan", self.port)


class BluetoothSender(Thread):
    def __init__(self, client_socket: BluetoothSocket, lora_input: Queue):
        Thread.__init__(self, daemon=True)
        self.setName("BluetoothSender")
        self.client_socket = client_socket
        self.stop_running = False
        self.lora_input = lora_input

    def run(self):
        while not self.stop_running:
            try:
                data = self.lora_input.get(timeout=2)
                try:
                    self.client_socket.send(data + "\n")
                except bluetooth.btcommon.BluetoothError:
                    break
            except queue.Empty:
                pass

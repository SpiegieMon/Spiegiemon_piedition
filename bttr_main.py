#!/usr/bin/python3
import bttr_sx126x
import os
from consolemenu import *
from consolemenu.items import *

ttydevices = ["/dev/ttyS0", "/dev/ttyAMA0"]

if os.path.exists(ttydevices[0]):
    ttydevice = ttydevices[0]
else:
    ttydevice = ttydevices[1]
node = bttr_sx126x.sx126x(serial_num = ttydevice,freq=868,addr=100,power=22,rssi=True)

def send(data):
    node.send(data)

def ui_send():
    pu = PromptUtils(Screen())
    # PromptUtils.input() returns an InputResult
    result = pu.input("Text: ")
    send(result.input_string)

def ui_recv():
    while True:
        node.receive()

menu = ConsoleMenu("Hauptmenue")

sendtext_item = FunctionItem("Text senden", ui_send)
recv_item = FunctionItem("Text empfangen", ui_recv)

menu.append_item(sendtext_item)
menu.append_item(recv_item)

menu.show()

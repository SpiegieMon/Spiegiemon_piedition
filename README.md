# Spiegiemon_PiEdition

Chat app for LoRa communication written in python with bluetooth communication or over console

Uses Raspberry Pi with LoRa module **sx1262**

# Prerequisites

In file /etc/bluetooth/main.conf

```txt
DiscoverableTimeout = 0
PairableTimeout = 0
```


In file /etc/systemd/system/dbus-org.bluez.service

Overwrite 
```ini
ExecStart=/usr/lib/bluetooth/bluetoothd
```
with
```ini
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

then restart services with 

```bash
sudo systemctl daemon-reload
sudo systemctl restart bluetooth.service
```

## Systemd unit-file
```ini
[Unit]
Description=SpiegieMon

[Service]
Type=simple
WorkingDirectory=/home/pi/git/Spiegiemon_piedition
ExecStart=/home/pi/git/Spiegiemon_piedition/main.py
 

[Install]
WantedBy=multi-user.target

```

# Features

- [x] threaded Bluetooth communication to module
- [x] threaded LoRa communication
- [x] queue based sending of messages so everything send by bluetooth gets send by LoRa-Module
- [x] console input 
- [ ] LoRa Repeater to increase range (first step of LoRa-Network)
- [ ] ACK between lora modules so no Messages get lost

# Tested with

Raspberry Pi 2 Model B Rev 1.2 using Raspbian 11
- with bluetooth dongle
Raspberry Pi 4 Model B Rev 1.2 using Raspbian 10
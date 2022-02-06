# Spiegiemon_PiEdition

Chat app for RaspberryPi LoRa communication written in python with bluetooth communication or over console

Uses Raspberry Pi with LoRa module **sx1262**

# Prerequisites

Package and ansiblescript should do everything automatically

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

to make Raspberry pi Bluetooth discoverable

## Systemd unit-file
```ini
[Unit]
Description=SpiegieMon

[Service]
Type=simple
WorkingDirectory=/home/pi/git/Spiegiemon_piedition
ExecStart=/home/pi/git/Spiegiemon_piedition/main.py
Environment="PYTHONUNBUFFERED=1"
After=bluetooth
Requires=bluetooth

[Install]
WantedBy=multi-user.target
```

# Message format
The message has the following format:
- One 1-bit message ID (incrementing for each message)
- One 

# Features

- [x] threaded Bluetooth communication to module
- [x] threaded LoRa communication
- [x] queue based sending of messages so everything send by bluetooth gets send by LoRa-Module
- [x] console input 
- [x] create systemd unit-file
- [x] create -i flag for interactive mode (console input)
- [ ] Kontroll-LED 
- [ ] autosend sendername over lora
- [ ] ACK between lora modules so no Message gets lost
- [ ] add configfile
- [ ] add ! commands to change sessionconfig in API like mannor (e.g. !setName:name or !getName)
- [ ] LoRa Repeater to increase range (first step of LoRa-Network)
- [ ] add ansible setupscript
- [ ] pack to dpkg package
- [ ] force LoRa airtime restrictions

# Tested with

- Raspberry Pi 2 Model B Rev 1.2 using Raspbian 11
(with bluetooth dongle)
- Raspberry Pi 4 Model B Rev 1.2 using Raspbian 10
- Raspberry Pi Zero W Rev 1.1 using Raspbian 11 (LoRa not confirmed yet)

# Contribution

If you want to contribute to this Project, you are welcome to fork this repository and submit a pull request.

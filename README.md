# Spiegiemon_piedition

Chatapp for lorawancommunication written in python with bluetooth communication or over console

used Lorawan module **sx1262**

# prerequisits

in file /etc/bluetooth/main.conf

DiscoverableTimeout = 0
PairableTimeout = 0


in file /etc/systemd/system/dbus-org.bluez.service

overwrite 
```txt
ExecStart=/usr/lib/bluetooth/bluetoothd
```
with
```txt
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

then restart services with 

```bash
sudo systemctl daemon-reload
sudo systemctl restart bluetooth.service
```


# Features

[x] threadded Bluetooth communication to modul
[x] threaded LoRa communication
[x] queue based sending of messages so everything send by bluetooth gets send by LoRa-Module
[x] console input 
[ ] LoRa Repeater to increase range (first step of LoRa-Network)
[ ] ACK between lora modules so no Messages get lost
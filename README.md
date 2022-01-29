# Spiegiemon_piedition

Chatapp for lorawancommunication written in python with bluetooth communication or over console

used Lorawan module **sx1262**

# prerequisits

in file /etc/bluetooth/main.conf

DiscoverableTimeout = 0
PairableTimeout = 0


in file /etc/systemd/system/dbus-org.bluez.service

overwrite 
```
ExecStart=/usr/lib/bluetooth/bluetoothd
```
with
```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

then restart services with 

```
sudo systemctl daemon-reload
sudo systemctl restart bluetooth.service
```


# Features
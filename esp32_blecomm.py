#!/usr/bin/python3
import sys, time
from bledevice import scanble, BLEDevice

if len(sys.argv) != 2:
    print("Usage: python blecomm.py <ble address>")
    print("Scan devices are as follows:")
    print(scanble(timeout=3))
    sys.exit(1)

esp32 = BLEDevice(sys.argv[1])
vh=esp32.getvaluehandle(b"6e400002")
#command = b"A"
while True:
    esp32.writecmd(vh, bytes("test\r\n".encode('utf-8')).hex())
    #esp32.writecmd(vh, command.hex())
    #print('Send: ' + str(command))
    #if command is b"A":
    #    command = b"B"
    #else:
    #    command = b"A"
    data = esp32.notify()
    if data is not None:
        print("Received: ", data)
    time.sleep(1)

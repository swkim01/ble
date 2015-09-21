#!/usr/bin/env python
import sys, time
from bledevice import scanble, BLEDevice

if len(sys.argv) != 2:
    print "Usage: python blecomm.py <ble address>"
    print "Scan devices are as follows:"
    print scanble(timeout=3)
    sys.exit(1)

hm10 = BLEDevice(sys.argv[1])
while True:
    vh=hm10.getvaluehandle("ffe1")
    hm10.writecmd(vh, "test\r\n".encode('hex'))
    data = hm10.notify()
    if data is not None:
        print "Received: ", data
    time.sleep(1)

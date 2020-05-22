#!/usr/bin/python3
import sys, time
import pygatt

if len(sys.argv) != 2:
    print("Usage: python blecomm.py <ble address>")
    sys.exit(1)

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    print("Received: ", value)
    

#try:
adapter.start()
hm10 = adapter.connect(sys.argv[1])
hm10.subscribe("0000ffe1-0000-1000-8000-00805f9b34fb", handle_data)

#finally:
#    adapter.stop()

while True:
    hm10.char_write("0000ffe1-0000-1000-8000-00805f9b34fb", b"test\r\n")
    time.sleep(1)

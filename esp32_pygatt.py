#!/usr/bin/python3
import sys, time
import pygatt

if len(sys.argv) != 2:
    print("Usage: python pygatt.py <ble address>")
    sys.exit(1)

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    print("Received: ", value)
    

#try:
adapter.start()
esp32 = adapter.connect(sys.argv[1])
esp32.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", handle_data)

#finally:
#    adapter.stop()

data = b"A"

while True:
    #esp32.char_write("6e400002-b5a3-f393-e0a9-e50e24dcca9e", b"test\r\n")
    esp32.char_write("6e400002-b5a3-f393-e0a9-e50e24dcca9e", data)
    print('Send: ' + str(data))
    if data is b"A":
        data = b"B"
    else:
        data = b"A"
    time.sleep(1)

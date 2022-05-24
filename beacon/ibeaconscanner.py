#!/usr/bin/python3

import re, sys
import pexpect

def measureDistance(txPower, rssi):
  if rssi == 0:
    return -1.0 # if we cannot determine accuracy, return -1.
  ratio = rssi * 1.0 / txPower
  if ratio < 1.0:
    return pow(ratio,10)
  else:
    return (0.89976) * pow(ratio, 7.7095) + 0.111

scan = pexpect.spawn("sudo hcitool lescan --duplicates 1>/dev/null")
p = pexpect.spawn("sudo hcidump --raw")
capturing = 0
packet = ""
while True:
    line = p.readline()
    if not line: break
    if capturing == 0:
        if line[0] == 62: #'>'
            packet = line[2:].strip().decode('utf-8')
            capturing = 1
    else:
        strline = line.strip().decode('utf-8')
        if re.match("^[0-9a-fA-F]{2}\ [0-9a-fA-F]", strline):
            packet += ' ' + strline
        elif re.match("^04\ 3E\ 2A\ 02\ 01\ .{26}\ 02\ 01\ .{14}\ 02\ 15", packet):
            #print("packet = " + packet)
            UUID=packet[69:116].replace(' ','')
            UUID=UUID[0:8]+'-'+UUID[8:12]+'-'+UUID[12:16]+'-'+UUID[16:20]+'-'+UUID[20:]
            MAJOR=int(packet[117:122].replace(' ',''),16)
            MINOR=int(packet[123:128].replace(' ',''),16)
            POWER=int(packet[129:131].replace(' ',''),16)-256
            RSSI=int(packet[132:134].replace(' ',''),16)-256
            if len(sys.argv) != 1 and sys.argv[1] == "-b" :
                print(UUID, MAJOR, MINOR, POWER, RSSI)
            else:
                print("UUID: %s MAJOR: %d MINOR: %d POWER: %d RSSI: %d" % (UUID, MAJOR, MINOR, POWER, RSSI))
            print("distance=", measureDistance(POWER, RSSI))
            capturing = 0
            packet=""
        elif len(packet) > 90:
            capturing = 0
            packet=""

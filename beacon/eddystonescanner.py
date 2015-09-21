#!/usr/bin/env python

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
        if line[0] == '>':
            packet = line[2:].strip()
            capturing = 1
    else:
        if re.match("^[0-9a-fA-F]{2}\ [0-9a-fA-F]", line.strip()):
            packet += ' ' + line.strip()
        elif re.match("^04\ 3E\ 29\ 02\ 01\ .{26}\ 02\ 01\ .{8}\ AA\ FE", packet):
            data = packet[51:]
            srv_ident = False
            dat_ident = False
            while True:
                if srv_ident != True or dat_ident != True:
                    length = int(data[0:2],16)
                    typeval = int(data[3:5],16)
                    ed_id = int(data[6:11].replace(' ',''),16)
                    if ed_id != 0xAAFE:
                        print "Error: %x is not eddystone id!" % (ed_id)
                        break
                    if typeval == 0x02 or typeval == 0x03: #list of 16bit Service UUIDs
                        srv_ident = True
                    elif typeval == 0x16: # service data
                        srvtype=int(data[12:14],16)
                        POWER=int(data[15:17].replace(' ',''),16)
                        if srvtype == 0x00: # Eddystone-UID
                            namespace=data[18:47].replace(' ','')
                            hidden=packet[21:23]+packet[24:26]+'-'+ \
                                   packet[27:29]+packet[30:32]+'-'+ \
                                   packet[33:35]+packet[36:38]
                            UUID=namespace[0:8]+'-'+hidden+'-'+namespace[8:]
                            INSTANCEID=data[48:65].replace(' ','')
                            if len(sys.argv) != 1 and sys.argv[1] == "-b" :
                                print UUID, INSTANCEID, POWER
                            else:
                                print "UUID: %s INSTANCEID: %s POWER: %d" % (UUID, INSTANCEID, POWER)
                        elif srvtype == 0x01: # Eddystone-URL
                            prefix=int(data[18:20].replace(' ',''),16)
                            URL=""
                            if prefix <= 3:
                                schemes=["http://www.", "https://www.", "http://", "https://"]
                                URL=schemes[prefix]
                            URL=URL+data[21:(length+1)*3].replace(' ','')
                            expansions=['.com/', '.org/', '.edu/', '.net/', \
                                        '.info/', '.biz/', '.gov/', \
                                        '.com', '.org', '.edu', '.net', \
                                        '.info', '.biz', '.gov']
                            for i in range(0x0d):
                                URL=URL.replace(i, expansions[i])

                            if len(sys.argv) != 1 and sys.argv[1] == "-b" :
                                print URL
                            else:
                                print "URL: %s" % (URL)

                        elif srvtype == 0x02: # Eddystone-TLM
                            pass
                        dat_ident = True
                    data = data[(length+1)*3:]
                else:
                    RSSI=int(data[0:2].replace(' ',''),16)
                    if len(sys.argv) != 1 and sys.argv[1] == "-b" :
                        print RSSI
                    else:
                        print "RSSI: %d" % (RSSI)
                    print "distance=", measureDistance(POWER, RSSI)
                    break
                capturing = 0
            print "packet = " + packet
            packet=""
        elif len(packet) > 90:
            capturing = 0
            packet=""

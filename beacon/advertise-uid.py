#!/usr/bin/python3
import sys
import subprocess
from optparse import OptionParser

parser = OptionParser(usage="%prog [options] [namespace] [instance]")

parser.add_option("-s", "--stop", dest="stop",
        action="store_true", default=False,
        help="Stop advertising")

parser.add_option("-v", "--verbose", dest="verbose",
        action="store_true", default=False,
        help="Print lots of debug output")

(options, args) = parser.parse_args()

# The default uid
uid_midfix = "-E7A7-4E14-BD99-"
namespace = "00112233445566778899"
instance = "AABBCCDDEEFF"

if len(args) > 0:
    namespace = args[0]
    instance = args[1]
    print(namespace, instance)

def verboseOutput(text):
    if options.verbose:
        sys.stderr.write(text + "\n")

def encodeUid(namespace, instance):
    data = []
    narray = map(ord, namespace.decode("hex"))
    data += narray
    iarray = map(ord, instance.decode("hex"))
    data += iarray
    return data

def encodeMessage(namespace, instance):
    encodedUid = encodeUid(namespace, instance)
    encodedUidLength = len(encodedUid)
    verboseOutput("Encoded uid length: " + str(encodedUidLength))
    if encodedUidLength != 16:
        raise Exception("Not encoded uid (16 bytes)")

    message = [
            0x02,   # Flags length
            0x01,   # Flags data type value
            0x1a,   # Flags data

            0x03,   # Service UUID length
            0x03,   # Service UUID data type value
            0xaa,   # 16-bit Eddystone UUID
            0xfe,   # 16-bit Eddystone UUID

            5 + len(encodedUid), # Service Data length
            0x16,   # Service Data data type value
            0xaa,   # 16-bit Eddystone UUID
            0xfe,   # 16-bit Eddystone UUID

            0x00,   # Eddystone-UID frame type
            0xed,   # txpower
            ]

    message += encodedUid
    message += [0x00, 0x00] # reserved

    return message

def systemCall(command):
    verboseOutput(command)
    child = subprocess.Popen(["-c", command],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True)
    child.communicate()

def advertise(namespace, instance):
    verboseOutput("Advertising: " + namespace + ", " + instance)
    message = encodeMessage(namespace, instance)

    # Prepend the length of the whole message
    message.insert(0, len(message))

    # Pad message to 32 bytes for hcitool
    while len(message) < 32: message.append(0x00)

    # Make a list of hex strings from the list of numbers
    message = map(lambda x: "%02x" % x, message)

    # Concatenate all the hex strings, separated by spaces
    message = " ".join(message)
    verboseOutput("Message: " + message)

    systemCall("sudo hciconfig hci0 up")
    # Stop advertising
    systemCall("sudo hcitool -i hci0 cmd 0x08 0x000a 00")

    # Set message
    systemCall("sudo hcitool -i hci0 cmd 0x08 0x0008 " + message)

    # Resume advertising
    systemCall("sudo hcitool -i hci0 cmd 0x08 0x000a 01")

def stopAdvertising():
    verboseOutput("Stopping advertising")
    systemCall("sudo hcitool -i hci0 cmd 0x08 0x000a 00")

try:
    if options.stop:
        stopAdvertising()
    else:
        advertise(namespace, instance)
except Exception as e:
    sys.stderr.write("Exception: " + str(e) + "\n")
    exit(1)

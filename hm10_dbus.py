#!/usr/bin/python3
import sys
import dbus
import time

# constants
BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'
DEVICE_IFACE = 'org.bluez.Device1'
DEVICE_PATH = '/org/bluez/hci0'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'

def read_value(bus_obj, data_path):
    """
    Read hm10
    :param bus_obj: Object of bus connected to
    :param data_path: The path to the data characteristic
    :return:
    """
    # Get device property interface
    char_props = dbus.Interface(bus_obj.get_object(BLUEZ_SERVICE_NAME, data_path),
                DBUS_PROP_IFACE)
    # Get characteristic interface for data
    data_iface = dbus.Interface(bus_obj.get_object(BLUEZ_SERVICE_NAME, data_path),
                GATT_CHRC_IFACE)
    # Read/write device data
    data_iface.ReadValue(dbus.Array())
    data_iface.WriteValue(b'test', dbus.Array())
    data_iface.StartNotify(dbus.Array())
    while True:
        value = char_props.Get(GATT_CHRC_IFACE, "Value")
        if value[0]:
            value_str = ''.join([chr(byte) for byte in value])
            #print("Received: ", value_str)
            print('Received: {0}'.format(value_str))
            data_iface.ReadValue(dbus.Array())
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 hm10_dbus.py <ble address>")
        sys.exit(1)

    bus = dbus.SystemBus()
    device_path = DEVICE_PATH + "/dev_" + sys.argv[1].replace(":","_")
    # Get property interface
    dev_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, device_path),
                DBUS_PROP_IFACE)
    #print(dir(dev_props))
    # Get characteristic interface for data
    dev_iface = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, device_path),
                DEVICE_IFACE)
    #print(dir(dev_iface))
    # Connect to device
    dev_iface.Connect()

    # Read the connected status property
    fetch_prop = 'Connected'
    device_data = dev_props.Get(DEVICE_IFACE, fetch_prop)
    print('Connected: {0}'.format(device_data))
    if device_data == 1:
        com_srv_path = device_path + '/service0010'
        com_data_path = com_srv_path + '/char0011'
        srv = bus.get_object(BLUEZ_SERVICE_NAME, com_srv_path)
        srv_props = srv.GetAll(GATT_SERVICE_IFACE, dbus_interface=DBUS_PROP_IFACE)
        chrc = bus.get_object(BLUEZ_SERVICE_NAME, com_data_path)
        chrc_props = chrc.GetAll(GATT_CHRC_IFACE, dbus_interface=DBUS_PROP_IFACE)
        read_value(bus, com_data_path)

    # Disconnect device
    dev_iface.Disconnect()

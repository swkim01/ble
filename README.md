# ble
Bluetooth LE related programs for Raspberry Pi/Linux.

- bledevice.py : basic class module for BLE devices
- blecomm.py : test program for communicating with an HM-10 BLE module
- blebulb.py : control program for Zengge BLE bulb
- yeelight.py : control program for Yeelight bedside lamp
- beacon : iBeacon and Google Eddystone related programs

To use these programs, you have to install bluez and python pexpect module.

The [bluez](http://www.elinux.org/RPi_Bluetooth_LE) (Bluetooth stack for linux) package can be installed by executing the following command:
````
sudo apt-get install bluetooth blueman bluez python-gobject python-gobject-2
````

The [pexpect](http://pexpect.readthedocs.org/en/stable/) module can be installed as follows:
````
sudo pip install pexpect
````

# BLE bulb Protocols
##[Zengge Bluetooth LED](http://www.enledcontroller.com/picture/show/164.aspx) 
<a id="Zengge BLE Protocol"></a>
Originally Zengge BLE bulb can be controlled by the [Magic Light](https://play.google.com/store/apps/details?id=com.Zengge.LEDBluetoothV2) app.
To execute our control program, use the following command.
````
python blebulb.py
````
<table>
  <tr>
    <th scope="col">Function</th><th scope="col">Command</th><th scope="col">Characteristic (Handle)</th><th scope="col">Data</th>
  </tr>
  <tr>
    <td>Power</td><td>Write</td><td>0xffe9 (0x43)</td>
    <td>STX(cc) : 0x24 : ETX(33)</br>Ex) Turn On : 0xcc2333, Turn Off: 0xcc2433</td>
  </tr>
  <tr>
    <td>RGB Light</td><td>Write</td><td>0xffe9 (0x43)</td>
    <td>STX(56) : R : G : B : 00 : f0 : ETX(aa)</br>Ex) Red :  0x56ff000000f0aa</br>Yellow : 0x56ffff0000f0aa, Blue: 0x560000ff00f0aa</td>
  </tr>
  <tr>
    <td>Warm Light</td><td>Write</td><td>0xffe9 (0x43)</td>
    <td>STX(56) : 00 00 00 : Lightness : 0f : ETX(aa)</br>Ex) 0x56000000ff0faa</td>
  </tr>
  <tr>
    <td>Set Mode</td><td>Write</td><td>0xffe9 (0x43)</td>
    <td>STX(bb) : Mode(25-38) : Speed(01-FF) : ETX(44)</br>Ex) 7 lights conversion(mode=0x25) : 0xbb250344</td>
  </tr>
  <tr>
    <td>Get State</td><td>Write and Read</td><td>0xffe9 (0x43)</br>0xffe4 (0x50)</td>
    <td>STX(ef) : 01 : ETX(77) = 0xef0177</br>Return: STX(66) 15 Power Mode 20 Speed R G B Lightness 06 ETX(99)</br>66 15 23 41 20 00 ff ff ff 00 06 99</br>66 15 23 25 20 05 ff ff ff 00 06 99 Mode(=0x25)</br>66 15 23 41 20 00 00 00 00 ff 06 99 Warm </td>
  </tr>
</table>

##[Yeelight Bedside Lamp](http://item.mi.com/1152300006.html) 
<a id="Yeelight BLE Protocol"></a>
Of course, Xiaomi's Yeelight Bedside Lamp can be controlled by the [Yeelight Lamp](https://play.google.com/store/apps/details?id=com.yeelight.cherry) app.
To execute our control program, use the following command.
````
python yeelight.py
````
<table>
  <tr>
    <th scope="col">Function</th><th scope="col">Command</th><th scope="col">Characteristic (Handle)</th><th scope="col">Data</th>
  </tr>
  <tr>
    <td>Certification</td><td>Write and Read</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x67) : ON(0x02) : ETX(00)\*15 - Total 18B</br>Return: STX(43) : CMD(0x63) : ON(0x02) : ETX(00)</td>
  </tr>
  <tr>
    <td>Power</td><td>Write</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x40) : ON(0x01)|OFF(0x02) : ETX(00)\*15 - Total 18B</br>Ex) Turn On : 0x434001000000000000000000000000000000</br>Turn Off: 0x434002000000000000000000000000000000</td>
  </tr>
  <tr>
    <td>RGB Light</td><td>Write</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x41) : R : G : B : 00 : 65 : ETX(00)\*11</br>Ex) Red :  0x4341ff000000650000000000000000000000</td>
  </tr>
  <tr>
    <td>Warm Light</td><td>Write</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x43) ; Color(2B, 1700~6500) : 65 : ETX(00)\*13</br>Ex) 0x43430400650000000000000000000000</td>
  </tr>
  <tr>
    <td>Lightness</td><td>Write</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x42) : Lightness : ETX(00)*15</br>The range of Lightness is 1 ~ 100</br>Ex) 0x434263000000000000000000000000000000</td>
  </tr>
</table>

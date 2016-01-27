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
    <th scope="col">기능</th><th scope="col">명령</th><th scope="col">특성 (핸들)</th><th scope="col">데이터</th>
  </tr>
  <tr>
    <td>전원</td><td>쓰기</td><td>0xffe9 (0x43)</td>
    <td>STX(cc) : 0x24 : ETX(33)</br>예) 켜기 : 0xcc2333, 끄기: 0xcc2433</td>
  </tr>
  <tr>
    <td>RGB 등</td><td>쓰기</td><td>0xffe9 (0x43)</td>
    <td>STX(56) : R : G : B : 00 : f0 : ETX(aa)</br>예) 빨강 :  0x56ff000000f0aa</br>노랑 : 0x56ffff0000f0aa, 파랑: 0x560000ff00f0aa</td>
  </tr>
  <tr>
    <td>Warm 등</td><td>쓰기</td><td>0xffe9 (0x43)</td>
    <td>STX(56) : 00 00 00 : 밝기 : 0f : ETX(aa)</br>예) 0x56000000ff0faa</td>
  </tr>
  <tr>
    <td>모드</td><td>쓰기</td><td>0xffe9 (0x43)</td>
    <td>STX(bb) : 모드(25-38) : 속도(01-FF) : ETX(44)</br>예) 7가지 색으로 변화(모드=0x25) : 0xbb250344</td>
  </tr>
  <tr>
    <td>상태 획득</td><td>쓰기 및 읽기</td><td>0xffe9 (0x43)</br>0xffe4 (0x50)</td>
    <td>STX(ef) : 01 : ETX(77) = 0xef0177</br>반환: STX(66) 15 전원 모드 20 속도 R G B 밝기 06 ETX(99)</br>66 15 23 41 20 00 ff ff ff 00 06 99</br>66 15 23 25 20 05 ff ff ff 00 06 99 모드 (0x25)</br>66 15 23 41 20 00 00 00 00 ff 06 99 Warm </td>
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
    <th scope="col">기능</th><th scope="col">명령</th><th scope="col">특성 (핸들)</th><th scope="col">데이터</th>
  </tr>
  <tr>
    <td>인증</td><td>쓰기 및 읽기</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x67) : ON(0x02) : ETX(00)\*15 - 총 18B</br>반환: STX(43) : CMD(0x63) : ON(0x02) : ETX(00)</td>
  </tr>
  <tr>
    <td>전원</td><td>쓰기</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x40) : ON(0x01)|OFF(0x02) : ETX(00)\*15 - 총 18B</br>예) 켜기 : 0x434001000000000000000000000000000000</br>끄기: 0x434002000000000000000000000000000000</td>
  </tr>
  <tr>
    <td>RGB 등</td><td>쓰기</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x41) : R : G : B : 00 : 65 : ETX(00)\*11</br>예) 빨강 :  0x4341ff000000650000000000000000000000</td>
  </tr>
  <tr>
    <td>Warm 등</td><td>쓰기</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x43) ; 색(2B, 1700~6500) : 65 : ETX(00)\*13</br>예) 0x43430400650000000000000000000000</td>
  </tr>
  <tr>
    <td>밝기</td><td>쓰기</td><td>0xaa7d3f34 (0x12)</td>
    <td>STX(43) : CMD(0x42) : 밝기 : ETX(00)*15</br>밝기 범위는 1 ~ 100</br>예) 0x434263000000000000000000000000000000</td>
  </tr>
</table>

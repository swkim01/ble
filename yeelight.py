from Tkinter import *
from tkColorChooser import askcolor
import colorsys
import math, sys, time
from bledevice import scanble, BLEDevice

bulb = None
WRITE_CHAR_UUID = "aa7d3f34" #-2d4f-41e0-807f-52fbf8cf7443"

COMMAND_STX = "43"
COMMAND_ETX = "00"

AUTH_CMD = "67"
AUTH_ON = "02"

POWER_CMD = "40"
POWER_ON = "01"
POWER_OFF = "02"

COLOR_CMD = "41"
RGB_MODE = "65"

BRIGHT_CMD = "42"

COLORTEMP_CMD = "43"
TEMP_MODE = "65"

COLORFLOW_CMD = "4a"

class ConnectPanel(Frame):
    def __init__(self, app):
        Frame.__init__(self, app)
        self.scanb = Button(self, text="Scan", command=self.scan)
        self.bl = StringVar()
        self.bles = OptionMenu(self, self.bl, ())
        self.connb = Button(self, text="Connect", command=self.connect)

        self.scanb.pack(side=LEFT)
        self.bles.pack(side=LEFT)
        self.connb.pack(side=RIGHT)

    def scan(self):
        bllist = scanble(timeout=2)
        print bllist
        if len(bllist) != 0:
            self.bl.set(bllist[0]['addr'])
            menu = self.bles['menu']
            menu.delete(0, 'end')
            for bl in bllist:
                menu.add_command(label=bl, command=lambda v=bl: self.bl.set(v['addr']))

    def connect(self):
        global bulb
        bulb = BLEDevice(self.bl.get())
        time.sleep(0.1)
        bulb.writereq(bulb.getvaluehandle(WRITE_CHAR_UUID), COMMAND_STX+AUTH_CMD+AUTH_ON+COMMAND_ETX*15)

class PowerPanel(Frame):
    def __init__(self, app):
        Frame.__init__(self, app)
        self.powerl = Label(self, text="Power")
        self.onb = Button(self, text="On", command=self.poweron)
        self.offb = Button(self, text="Off", command=self.poweroff)

        self.powerl.pack(side=LEFT)
        self.offb.pack(side=RIGHT)
        self.onb.pack(side=RIGHT)

    def poweron(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR_UUID), COMMAND_STX+POWER_CMD+POWER_ON+COMMAND_ETX*15)

    def poweroff(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR_UUID), COMMAND_STX+POWER_CMD+POWER_OFF+COMMAND_ETX*15)

class RgbPanel(Frame):
    def __init__(self, app):
        Frame.__init__(self, app)
        self.rgbl = Label(self, text="RGB")
        self.color = ((255, 255, 255), '#ffffff')
        self.selectb = Button(self, text="Select", command=self.getcolor)
        self.coll = Label(self, text="         ", bg="#FFFFFF")
        self.setb = Button(self, text="Set", command=self.setrgb)

        self.rgbl.pack(side=LEFT)
        self.setb.pack(side=RIGHT)
        self.coll.pack(side=RIGHT)
        self.selectb.pack(side=RIGHT)

    def getcolor(self):
        self.color = askcolor()
        print "color is ", self.color
        self.coll.configure(bg=self.color[1])

    def setrgb(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR_UUID), COMMAND_STX+COLOR_CMD+self.color[1][1:]+"00"+RGB_MODE+COMMAND_ETX*11)

class BrightnessPanel(Frame):
    def __init__(self, app):
        Frame.__init__(self, app)
        self.brightl = Label(self, text="Brightness")
        self.value = DoubleVar()
        self.value.set(1.0)
        self.scale = Scale(self, variable=self.value, from_=0.0, to=1.0, resolution=0.01, orient=HORIZONTAL)
        self.setb = Button(self, text="Set", command=self.setvalue)

        self.brightl.pack(side=LEFT)
        self.setb.pack(side=RIGHT)
        self.scale.pack(side=RIGHT)

    def setvalue(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR_UUID), COMMAND_STX+BRIGHT_CMD+("%02x"%(self.value.get()*100))+COMMAND_ETX*15)

class WarmPanel(Frame):
    def __init__(self, app):
        Frame.__init__(self, app)
        self.warml = Label(self, text="Warm")
        self.color = DoubleVar()
        self.color.set(1.0)
        self.scale = Scale(self, variable=self.color, from_=0.0, to=1.0, resolution=0.01, command=self.changecolor, orient=HORIZONTAL)
        self.setb = Button(self, text="Set", command=self.setwarm)

        self.warml.pack(side=LEFT)
        self.setb.pack(side=RIGHT)
        self.scale.pack(side=RIGHT)

    def changecolor(self, v):
        value = self.color.get()*255
        color = "#FFFF%02x" % (value)
        self.scale.configure(bg=color)

    def setwarm(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR_UUID), COMMAND_STX+COLORTEMP_CMD+("%04x"%(1700+self.color.get()*4800))+TEMP_MODE+COMMAND_ETX*13)

if __name__ == "__main__":
    tk = Tk()
    tk.title("Yeelight Bedside Lamp")

    connectp = ConnectPanel(tk)
    connectp.pack()
    powerp = PowerPanel(tk)
    powerp.pack(fill="both")
    rgbp = RgbPanel(tk)
    rgbp.pack(fill="both")
    brightp = BrightnessPanel(tk)
    brightp.pack(fill="both")
    warmp = WarmPanel(tk)
    warmp.pack(fill="both")

    def shutdown():
        tk.destroy()

    tk.protocol("WM_DELETE_WINDOW", shutdown)
    tk.mainloop()

from Tkinter import *
from tkColorChooser import askcolor
import colorsys
import math, sys, time
from bledevice import scanble, BLEDevice

bulb = None
WRITE_CHAR = "ffe9"
READ_CHAR = "ffe4"

POWER_STX = "cc"
POWER_ETX = "33"
POWER_ON = "23"
POWER_OFF = "24"

LIGHT_STX = "56"
LIGHT_ETX = "aa"
RGB_MODE = "f0"
WARM_MODE = "0f"

MODE_STX = "bb"
MODE_ETX = "44"

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
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR), POWER_STX+POWER_ON+POWER_ETX)

    def poweroff(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR), POWER_STX+POWER_OFF+POWER_ETX)

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
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR), LIGHT_STX+self.color[1][1:]+"00"+RGB_MODE+LIGHT_ETX)

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
        color = "#%02x%02x00" % (value, value)
        #print "color is ", color
        self.scale.configure(bg=color)

    def setwarm(self):
        global bulb
        bulb.writecmd(bulb.getvaluehandle(WRITE_CHAR), LIGHT_STX+"000000"+("%02x"%(self.color.get()*255))+WARM_MODE+LIGHT_ETX)

tk = Tk()
tk.title("BLE Light Bulb")

connectp = ConnectPanel(tk)
connectp.pack()
powerp = PowerPanel(tk)
powerp.pack(fill="both")
rgbp = RgbPanel(tk)
rgbp.pack(fill="both")
warmp = WarmPanel(tk)
warmp.pack(fill="both")

def shutdown():
    tk.destroy()

tk.protocol("WM_DELETE_WINDOW", shutdown)
tk.mainloop()

# Copyright (c) 2016 Sebastian Kanis
# This file is part of pi-led-control.

# pi-led-control is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pi-led-control is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pi-led-control.  If not, see <http://www.gnu.org/licenses/>.

class ColorSetter():

    def __init__(self, printInfo, brightness):
        self._printInfo = printInfo
        self._currentColor = None
        self.setBrightness(brightness)
        
    def setBrightness(self, brightness):
        self._brightness = min(1, max(0, brightness))
        if self._currentColor != None:
            print("resetting color after brightness change {}, {}".format(self._brightness, self._currentColor))
            self.setColorRGB(self._currentColor[0], self._currentColor[1],self._currentColor[2]) 

    def getBrightness(self):
        return self._brightness

    def _rgbBound(self, value):
        return min(255, max(0, value))

    def setColorRGB(self, r, g, b, s=1):
        r = self._rgbBound(r)/255
        g = self._rgbBound(g)/255
        b = self._rgbBound(b)/255
        s = min(1, max(0, s))
        self.setColor(r * s, g * s, b * s)


    def setColor(self, r,g,b):
        if r != None:
            with open("/dev/pi-blaster", "w") as piblaster:
                print("17={}".format(r*self._brightness), file=piblaster)
                if self._printInfo:
                    print("r: {} ".format(r*self._brightness) ,end="",flush=True)
        if g != None:
            with open("/dev/pi-blaster", "w") as piblaster:
                print("22={}".format(g*self._brightness), file=piblaster)
                if self._printInfo:
                    print("g: {} ".format(g*self._brightness) ,end="",flush=True)
        if b != None:
            with open("/dev/pi-blaster", "w") as piblaster:
                print("24={}".format(b*self._brightness), file=piblaster)
                if self._printInfo:
                    print("b: {}".format(b*self._brightness) ,end="",flush=True)
        self._currentColor = (round(r*255), round(g*255), round(b*255))
        if self._printInfo:
            print("")
            
    def getCurrentColor(self):
        return self._currentColor

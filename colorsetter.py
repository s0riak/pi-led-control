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
from ledstate import LEDState

class ColorSetter():

    def __init__(self, printInfo, brightness):
        self._printInfo = printInfo
        self._ledState = LEDState()
        self._ledState.brightness = brightness

    def setBrightness(self, brightness):
        self._ledState.brightness = brightness
        if self._ledState.isComplete():
            print("resetting color after brightness change {}, {}".format(self._ledState.brightness, self._ledState.getColor()))
            self.setValue(self._ledState)

    def getBrightness(self):
        return self._ledState.brightness

    def _writePiBlasterValue(self, channel, channelName, value):
        with open("/dev/pi-blaster", "w") as piblaster:
            print("{}={}".format(channel, value), file=piblaster)
            if self._printInfo:
                print("{}: {} ".format(channelName, value) ,end="",flush=True)

    def setValue(self, ledState):
        self._ledState.updateAvailableValues(ledState)
        if self._ledState.isComplete():
            self._writePiBlasterValue(17, "red" , self._ledState.red*self._ledState.brightness)
            self._writePiBlasterValue(22, "green" , self._ledState.green*self._ledState.brightness)
            self._writePiBlasterValue(24, "blue" , self._ledState.blue*self._ledState.brightness)
        if self._printInfo:
            print("")
            
    def getCurrentValue(self):
        return self._ledState

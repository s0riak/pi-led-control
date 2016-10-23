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
from server.ledstate import LEDState
import logging

class ColorSetter():

    def __init__(self, brightness):
        self._ledState = LEDState()
        self._ledState.brightness = brightness
        self._colorRounding = 5

    def setBrightness(self, brightness):
        self._ledState.brightness = brightness
        if self._ledState.isComplete():
            logging.info("resetting color after brightness change {}, {}".format(self._ledState.brightness, self._ledState.getColor()))
            self.setValue(self._ledState)

    def getBrightness(self):
        return self._ledState.brightness

    def _writePiBlasterValue(self, channel, channelName, value):
        with open("/dev/pi-blaster", "w") as piblaster:
            print("{}={}".format(channel, value), file=piblaster)

    def setValue(self, ledState):
        self._ledState.updateAvailableValues(ledState)
        if self._ledState.isComplete():
            redValue = round(self._ledState.red*self._ledState.brightness, self._colorRounding)
            greenValue = round(self._ledState.green*self._ledState.brightness, self._colorRounding)
            blueValue = round(self._ledState.blue*self._ledState.brightness, self._colorRounding)
            self._writePiBlasterValue(17, "red" , redValue)
            self._writePiBlasterValue(22, "green" , greenValue)
            self._writePiBlasterValue(24, "blue" , blueValue)
            logging.debug("updated pi-blaster: red={}, green={}, blue={}".format(redValue, greenValue, blueValue))
            
    def getCurrentValue(self):
        return self._ledState

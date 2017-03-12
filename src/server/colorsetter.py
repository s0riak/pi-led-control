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
import logging
import traceback

from server.exceptions.piblasterunavailableexception import PiBlasterUnavailableException
from server.ledstate import LEDState
from server.crossbarintegration import statuspublisher


class ColorSetter:

    def __init__(self, brightness):
        self._ledState = LEDState()
        self._ledState.brightness = brightness
        self._colorRounding = 5

    def setBrightness(self, brightness):
        self._ledState.brightness = brightness
        if self._ledState.isComplete():
            logging.getLogger("main").info("resetting color after brightness change {}, {}".format(self._ledState.brightness, self._ledState.getColor()))
            self.setValue(self._ledState)

    def getBrightness(self):
        return self._ledState.brightness

    def _writePiBlasterValue(self, channel, channelName, value):
        piBlasterPath = "/dev/pi-blaster"
        try:
            piblaster = open(piBlasterPath, "w")
        except:
            self._ledState = LEDState()
            errorMessage = "error opening " + piBlasterPath + " " + traceback.format_exc()
            raise PiBlasterUnavailableException(errorMessage)
        else:
            try:
                print("{}={}".format(channel, value), file=piblaster)
                piblaster.close()
            except:
                self._ledState = LEDState()
                errorMessage = "error writing {}={} to {} ({})".format(channel, value, piBlasterPath, channelName)
                piblaster.close()
                raise PiBlasterUnavailableException(errorMessage)      

    def setValue(self, ledState):
        if ledState.brightness is not None and ledState.brightness != self._ledState.brightness:
            logging.getLogger("main").warning("updating brightness in setValue from " + str(self._ledState.brightness) + " to " + str(ledState.brightness))
        self._ledState.updateAvailableValues(ledState)
        if self._ledState.isComplete():
            redValue = round(self._ledState.red*self._ledState.brightness, self._colorRounding)
            greenValue = round(self._ledState.green*self._ledState.brightness, self._colorRounding)
            blueValue = round(self._ledState.blue*self._ledState.brightness, self._colorRounding)
            self._writePiBlasterValue(17, "red" , redValue)
            self._writePiBlasterValue(22, "green" , greenValue)
            self._writePiBlasterValue(24, "blue" , blueValue)
            logging.getLogger("main").debug("updated pi-blaster: red={}, green={}, blue={}".format(redValue, greenValue, blueValue))
            try:
                statuspublisher.getStatusPublisher().publishStatus()
            except Exception as e:
                logging.getLogger("main").warning("Error during publishStatus " + str(e))
                
            
    def getCurrentValue(self):
        return self._ledState

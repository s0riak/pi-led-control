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

from server.colorfilters.polynomialbrightnessfilter import PolynomialBrightnessFilter
from server.crossbarintegration import statuspublisher
from server.exceptions.piblasterunavailableexception import PiBlasterUnavailableException
from server.ledstate import LEDState


class ColorSetter:
    def __init__(self, brightness):
        self._ledState = LEDState()
        self._ledState.brightness = brightness
        self._colorRounding = 5

    def setBrightness(self, brightness):
        self._ledState.brightness = brightness
        if self._ledState.isComplete():
            logging.getLogger("main").info(
                "resetting color after brightness change {}, {}".format(
                    self._ledState.brightness,
                    self._ledState.getColor()))
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

    def getValueForPiBlaster(self):
        myFilter = PolynomialBrightnessFilter(2.0)
        filteredState = myFilter.filter(self._ledState)
        return {"red": round(filteredState.red * filteredState.brightness,
                             self._colorRounding),
                "green": round(filteredState.green * filteredState.brightness,
                               self._colorRounding),
                "blue": round(filteredState.blue * filteredState.brightness,
                              self._colorRounding)}

    def setValue(self, ledState):
        if (ledState.brightness is not None and
                    ledState.brightness != self._ledState.brightness):
            logging.getLogger("main").warning(
                "updating brightness in setValue from "
                + str(self._ledState.brightness)
                + " to " + str(ledState.brightness))
        self._ledState.updateAvailableValues(ledState)
        if self._ledState.isComplete():
            piValue = self.getValueForPiBlaster()
            self._writePiBlasterValue(17, "red", piValue["red"])
            self._writePiBlasterValue(22, "green", piValue["green"])
            self._writePiBlasterValue(24, "blue", piValue["blue"])
            logging.getLogger("main").debug(
                "updated pi-blaster: red={}, green={}, blue={}".format(
                    piValue["red"], piValue["green"], piValue["blue"]))
            try:
                statuspublisher.getStatusPublisher().publishStatus()
            except Exception as e:
                logging.getLogger("main").warning("Error during publishStatus " + str(e))

    def getCurrentValue(self):
        return self._ledState

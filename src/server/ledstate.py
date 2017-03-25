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


def validateValue(value):
    if not isinstance(value, float):
        raise TypeError("LEDValue only accepts floats, got " + str(value))
    if value < 0 or value > 1:
        raise ValueError("LEDValue only accepts floats between 0 and 1, got " + str(value))


class LEDState:
    # all values handled by this class are between 0 and 1 any other value cause an error

    def __str__(self):
        return "red: {}, green: {}, blue: {}, brightness: {}".format(self.red, self.green, self.blue, self.brightness)

    def __repr__(self):
        return self.__str__()

    def __init__(self, red=None, green=None, blue=None, brightness=None):
        if red is None:
            self.__red = None
        else:
            validateValue(red)
            self.__red = red
        if green is None:
            self.__green = None
        else:
            validateValue(green)
            self.__green = green
        if blue is None:
            self.__blue = None
        else:
            validateValue(blue)
            self.__blue = blue
        if brightness is None:
            self.__brightness = None
        else:
            validateValue(brightness)
            self.__brightness = brightness

    def __getRed(self):
        return self.__red

    def __setRed(self, red):
        validateValue(red)
        self.__red = red

    red = property(__getRed, __setRed)

    def __getGreen(self):
        return self.__green

    def __setGreen(self, green):
        validateValue(green)
        self.__green = green

    green = property(__getGreen, __setGreen)

    def __getBlue(self):
        return self.__blue

    def __setBlue(self, blue):
        validateValue(blue)
        self.__blue = blue

    blue = property(__getBlue, __setBlue)

    def __getBrightness(self):
        return self.__brightness

    def __setBrightness(self, brightness):
        validateValue(brightness)
        self.__brightness = brightness

    brightness = property(__getBrightness, __setBrightness)

    def isComplete(self):
        return self.red is not None and self.green is not None and self.blue is not None and self.brightness is not None

    def getColor(self):
        return [self.__getRed(), self.__getGreen(), self.__getBlue()]

    def updateAvailableValues(self, newState):
        if newState.red is not None:
            self.red = newState.red
        if newState.green is not None:
            self.green = newState.green
        if newState.blue is not None:
            self.blue = newState.blue
        if newState.brightness is not None:
            self.brightness = newState.brightness

    # doesn't take brightness into account for equality check
    def colorsEqual(self, comparedState):
        if self.red != comparedState.red:
            return False
        if self.green != comparedState.green:
            return False
        if self.blue != comparedState.blue:
            return False
        return True

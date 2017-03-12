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

import copy
import logging

from server.ledstate import LEDState
from server.programs.abstractprogram import AbstractProgram


def getInterpolationValue(currentValue, nextValue, pointIndex, numberOfPoints):
    if currentValue == nextValue:
        return nextValue
    else:
        new_value = currentValue + ((nextValue - currentValue) / numberOfPoints) * pointIndex
        if new_value > 1.0:
            return 1.0
        elif new_value < 0.0:
            return 0.0
        else:
            return new_value

def getInterpolationPoint(currentPoint, nextPoint, pointIndex, numberOfPoints):
    red = getInterpolationValue(currentPoint.red, nextPoint.red, pointIndex, numberOfPoints)
    green = getInterpolationValue(currentPoint.green, nextPoint.green, pointIndex, numberOfPoints)
    blue = getInterpolationValue(currentPoint.blue, nextPoint.blue, pointIndex, numberOfPoints)
    if not nextPoint.brightness is None:
        brightness = getInterpolationValue(currentPoint.brightness, nextPoint.brightness, pointIndex, numberOfPoints)
    else:
        brightness = currentPoint.brightness
    return LEDState(red, green, blue, brightness)


class ColorPathProgram(AbstractProgram):

    class PathIterator:
        def __init__(self, colorPath):
            self._colorPath = colorPath
            self._currentIndex = -1
        def __iter__(self):
            return self
        def __next__(self):
            self._currentIndex += 1
            if self._currentIndex >= len(self._colorPath):
                raise StopIteration
            return self._colorPath[self._currentIndex]
        def __repr__(self):
            result = "PathIterator: "
            for color in self._colorPath:
                result = result + str(color) + " "
            return result
            
    #timePerColor is the time the color is shown at each interpolationPoint not for one point on the colorpath
    def __init__(self, colorPath, interpolationPoints, timePerColor, startFromCurrent=False):
        super().__init__()
        self._colorPath = colorPath
        self._interpolationPoints = interpolationPoints
        self._timePerColor = timePerColor
        self._startFromCurrent = startFromCurrent

    def initColorIterator(self, colorPath):
        self._colorIterator = ColorPathProgram.PathIterator(colorPath)
        
    def setTimePerColor(self, timePerColor):
        self._timePerColor = timePerColor

    def run(self):
        if self._startFromCurrent:
            if self._lastValue is not None and self._lastValue.isComplete():
                if not self._colorPath[0].colorsEqual(self._lastValue):
                    self._colorPath.insert(0, copy.deepcopy(self._lastValue))
            else:
                logging.getLogger("main").warning("last color not available")
        self.initColorIterator(self._colorPath)
        currentPoint = None
        for color in self._colorIterator:
            if currentPoint is None:
                currentPoint = color
                continue
            nextPoint = color
            for j in range(0, self._interpolationPoints+1):
                self._setValue(getInterpolationPoint(currentPoint, nextPoint, j, self._interpolationPoints))
                self._waitIfNotStopped(self._timePerColor)
            currentPoint = color
            
        currentPoint = self._colorPath[-1]
        self._setValue(currentPoint)

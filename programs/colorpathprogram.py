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

from ledstate import LEDState
from programs.abstractprogram import AbstractProgram

class ColorPathProgram(AbstractProgram):

    class PathIterator:
        def __init__(self, colorPath):
            self._colorPath = colorPath
            self._currentIndex = -1
        def __iter__(self):
            return self
        def __next__(self):
            self._currentIndex = self._currentIndex +1
            if self._currentIndex >= len(self._colorPath):
                raise StopIteration
            return self._colorPath[self._currentIndex]
        def __repr__(self):
            result = "PathIterator: "
            for color in self._colorPath:
                result = result + str(color) + " "
            return result
            
    #timePerColor is the time the color is shown at each interpolationPoint not for one point on the colorpath
    def __init__(self, printInfo, colorPath, interpolationPoints, timePerColor, startFromCurrent=False):
        super().__init__(printInfo)
        self._colorPath = colorPath
        self._interpolationPoints = interpolationPoints
        self._timePerColor = timePerColor
        self._startFromCurrent = startFromCurrent

    def initColorIterator(self, colorPath):
        self._colorIterator = ColorPathProgram.PathIterator(colorPath)
        
    def setTimePerColor(self, timePerColor):
        self._timePerColor = timePerColor

    def __getInterpolationValue(self, currentValue, nextValue, pointIndex, numberOfPoints):
        if currentValue == nextValue:
            return nextValue
        else:
            return currentValue + ((nextValue - currentValue)/numberOfPoints)*pointIndex
        
    def __getInterpolationPoint(self, currentPoint, nextPoint, pointIndex, numberOfPoints):
        red = self.__getInterpolationValue(currentPoint.red, nextPoint.red, pointIndex, numberOfPoints)
        green = self.__getInterpolationValue(currentPoint.green, nextPoint.green, pointIndex, numberOfPoints)
        blue = self.__getInterpolationValue(currentPoint.blue, nextPoint.blue, pointIndex, numberOfPoints)
        if not nextPoint.brightness == None:
            brightness = self.__getInterpolationValue(currentPoint.brightness, nextPoint.brightness, pointIndex, numberOfPoints)
        else:
            brightness = currentPoint.brightness
        return LEDState(red, green, blue, brightness)
        
    def run(self):
        if self._startFromCurrent:
            if self._lastValue != None and self._lastValue.isComplete():
                if not self._colorPath[0].colorsEqual(self._lastValue):
                    self._colorPath.insert(0, copy.deepcopy(self._lastValue))
            else:
                print("warning last color not available")
        self.initColorIterator(self._colorPath)
        currentPoint = None
        for color in self._colorIterator:
            if currentPoint == None:
                currentPoint = color
                continue
            nextPoint = color
            for j in range(0, self._interpolationPoints+1):
                self._setValue(self.__getInterpolationPoint(currentPoint, nextPoint, j, self._interpolationPoints))
                self._waitIfNotStopped(self._timePerColor)
            currentPoint = color
            
        currentPoint = self._colorPath[-1]
        self._setValue(currentPoint)

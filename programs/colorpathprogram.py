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
        
    def run(self):
        if self._startFromCurrent:
            if self._lastColor != None:
                if self._lastColor[0] != None and self._lastColor[1] != None and self._lastColor[2] != None:
                    self._colorPath.insert(0, self._lastColor)
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
                interpolationPoint = {}
                if nextPoint[0] == currentPoint[0]:
                    interpolationPoint[0] = nextPoint[0]
                else:
                    interpolationPoint[0] = currentPoint[0]+ ((nextPoint[0] - currentPoint[0])/self._interpolationPoints)*j
                if nextPoint[1] == currentPoint[1]:
                    interpolationPoint[1] = nextPoint[1]
                else:
                    interpolationPoint[1] = currentPoint[1]+ ((nextPoint[1] - currentPoint[1])/self._interpolationPoints)*j
                if nextPoint[2] == currentPoint[2]:
                    interpolationPoint[2] = nextPoint[2]
                else:
                    interpolationPoint[2] = currentPoint[2]+ ((nextPoint[2] - currentPoint[2])/self._interpolationPoints)*j
                self._setColorRGB(interpolationPoint[0], interpolationPoint[1], interpolationPoint[2])
                self._waitIfNotStopped(self._timePerColor)
            currentPoint = color
            
        currentPoint = self._colorPath[-1]
        self._setColorRGB(currentPoint[0], currentPoint[1], currentPoint[2])

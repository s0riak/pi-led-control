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

import random
from server.programs.colorpathprogram import ColorPathProgram
class RandomPathProgram(ColorPathProgram):

    class RandomIterator:
        def __init__(self, colorSet):
            self._colorSet = colorSet
            self._iteration = 0
            self._nextItem = None
        def __iter__(self):
            return self
        def __next__(self):
            #only change the color every second point
            if self._iteration % 2 == 0:
                newItem = random.choice(self._colorSet)
                #make sure the next point differs from the current point
                while(self._nextItem == newItem):
                    newItem = random.choice(self._colorSet)
                self._nextItem = newItem
            self._iteration = self._iteration + 1
            return self._nextItem

    def __init__(self, colorSet, durationPerPoint):
        interpolationPoints = 60
        durationPerInterpolationPoint = durationPerPoint / interpolationPoints
        super().__init__(colorSet, interpolationPoints, durationPerInterpolationPoint)

    def initColorIterator(self, colorPath):
        self._colorIterator = RandomPathProgram.RandomIterator(colorPath)

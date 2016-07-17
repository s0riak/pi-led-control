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
from programs.randompathprogram import RandomPathProgram
class RandomPathSleepProgram(randomPathPathProgram):

    class RandomIterator:
        def __init__(self, colorSet, self._sleepTimer, self._durationPerPoint):
            self._colorSet = colorSet
            self._iteration = 0
            self._nextItem = None
            self._sleepTimer
        def __iter__(self):
            return self
        def __next__(self):
            s
            #only change the color every second point
            if self._iteration % 2 == 0:
                self._nextItem = random.choice(self._colorSet)
            self._iteration = self._iteration + 1
            return self._nextItem

    def __init__(self, printInfo, colorSet, durationPerPoint, sleepTimer):
        interpolationPoints = 60
        durationPerInterpolationPoint = durationPerPoint / interpolationPoints
        self._durationPerPoint = durationPerPoint
        self._sleepTimer = sleepTimer
        super().__init__(printInfo, colorSet, interpolationPoints, durationPerInterpolationPoint)

    def initColorIterator(self, colorPath):
        self._colorIterator = RandomPathProgram.RandomIterator(colorPath, self._sleepTimer, self._durationPerPoint)

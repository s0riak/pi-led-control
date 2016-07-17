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
from programs.abstractprogram import AbstractProgram
class RandomColorProgram(AbstractProgram):

    def __init__(self, printInfo, minColor, maxColor, secondsPerColor):
        super().__init__(printInfo)
        self._minColor = minColor
        self._maxColor = maxColor
        self._secondsPerColor = secondsPerColor

    def run(self):
        r = round(random.uniform(self._minColor, self._maxColor), 3)
        g = round(random.uniform(self._minColor, self._maxColor), 3)
        b = round(random.uniform(self._minColor, self._maxColor), 3)
        if self.printInfo:
            print("r: {}, g: {}, b: {}".format(r,g,b))
        self._setColor(r, g, b)
        self._waitIfNotStopped(self._secondsPerColor)

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
from random import randint
import random

from server.programs.abstractprogram import AbstractProgram


class SmoothRandomProgram(AbstractProgram):

    def __init__(self, maxDiff, secondsPerColor):
        super().__init__()
        self._maxDiff = maxDiff
        self._secondsPerColor = secondsPerColor

    def _getNextValue(self, oldValue):
        return max(0, min(1, oldValue + round(random.uniform(-1*self._maxDiff, self._maxDiff),3)))

    def run(self):
        r = round(random.uniform(0.0, 0.5), 3)
        g = round(random.uniform(0.0, 0.5), 3)
        b = round(random.uniform(0.0, 0.5), 3)
        while True:
            logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
            self._setColor(r, g, b)
            self._waitIfNotStopped(0.05)
            colorRand = randint(0,2)
            if colorRand == 0:
                r = self._getNextValue(r)
            elif colorRand == 1:
                g = self._getNextValue(g)
            else:
                b = self._getNextValue(b)

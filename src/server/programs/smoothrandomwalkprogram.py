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

from random import randint
import random

from server.programs.abstractprogram import AbstractProgram
import logging


class SmoothRandomWalkProgram(AbstractProgram):

    def __init__(self, maxDiff, secondsPerColor):
        super().__init__()
        self._maxDiff = maxDiff
        self._secondsPerColor = secondsPerColor

    def run(self):
        r = round(random.uniform(0.0, 0.5), 3)
        g = round(random.uniform(0.0, 0.5), 3)
        b = round(random.uniform(0.0, 0.5), 3)
        stepsInOneDirection = 50
        while True:
            colorRand = randint(0,2)
            upDownRand = bool(random.getrandbits(1))
            if colorRand == 0:
                if upDownRand:
                    for i in range(0,stepsInOneDirection):
                        r = max(0, r - round(random.uniform(0, self._maxDiff),3))
                        logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                        self._setColor(r, g, b)
                        self._waitIfNotStopped(self._secondsPerColor)
                        if r == 0:
                            break
                else:
                    for i in range(0,stepsInOneDirection):
                        r = min(1, r + round(random.uniform(0, self._maxDiff),3))
                        logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                        self._setColor(r, g, b)
                        self._waitIfNotStopped(self._secondsPerColor)
                        if r == 1:
                            break
            elif colorRand == 1:
                if upDownRand:
                    for i in range(0,stepsInOneDirection):
                        g = max(0, r - round(random.uniform(0, self._maxDiff),3))
                        logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                        self._setColor(r, g, b)
                        self._waitIfNotStopped(self._secondsPerColor)
                        if r == 0:
                            break
                if upDownRand:
                    for i in range(0,stepsInOneDirection):
                        g = min(1, r + round(random.uniform(0, self._maxDiff),3))
                        logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                        self._setColor(r, g, b)
                        self._waitIfNotStopped(self._secondsPerColor)
                        if r == 1:
                            break
            else:
                if upDownRand:
                    for i in range(0,stepsInOneDirection):
                        b = max(0, r - round(random.uniform(0, self._maxDiff),3))
                        logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                        self._setColor(r, g, b)
                        self._waitIfNotStopped(self._secondsPerColor)
                        if r == 0:
                            break
                if upDownRand:
                    for i in range(0,stepsInOneDirection):
                        b = min(1, r + round(random.uniform(0, self._maxDiff),3))
                        logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                        self._setColor(r, g, b)
                        self._waitIfNotStopped(self._secondsPerColor)
                        if r == 1:
                            break

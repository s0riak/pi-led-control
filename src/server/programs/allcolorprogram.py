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

from server.ledstate import LEDState
from server.programs.abstractprogram import AbstractProgram


class AllColorProgram(AbstractProgram):

    def __init__(self, stepsPerColor, secondsPerColor):
        super().__init__()
        self.stepsPerColor = stepsPerColor
        self.secondsPerColor = secondsPerColor

    def run(self):
        self._waitIfNotStopped(self.secondsPerColor)
        for i in range(0, self.stepsPerColor):
            for j in range(0, self.stepsPerColor):
                for k in range(0, self.stepsPerColor):
                    r = i/(self.stepsPerColor-1)
                    g = j/(self.stepsPerColor-1)
                    b = k/(self.stepsPerColor-1)
                    logging.getLogger("main").debug("r: {}, g: {}, b: {}".format(r,g,b))
                    self._setValue(LEDState(r, g, b, 1.0))
                    self._waitIfNotStopped(self.secondsPerColor)
        self._setValue(LEDState(0.0, 0.0, 0.0, 1.0))

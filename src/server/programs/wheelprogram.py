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

from server.ledstate import LEDState
from server.programs.colorpathprogram import ColorPathProgram
from server.programs.loopedprogram import LoopedProgram

class WheelProgram(LoopedProgram):

    #iterations number of wheel loops
    #minValue the minimum brightness
    #maxValue the maximum brightness
    #timePerColor the time per main color (not interpolation points)
    def __init__(self, iterations, minValue, maxValue, timePerColor):
        self._minValue = min(1.0, max(0.0, minValue))
        self._maxValue = min(1.0, max(0.0, maxValue))
        colorPath = [LEDState(maxValue,minValue,minValue),LEDState(minValue,maxValue,minValue),LEDState(minValue, minValue, maxValue)]
        interpolationsPoints = 30
        program = ColorPathProgram(colorPath, interpolationsPoints, float(timePerColor)/float(interpolationsPoints), True)
        
        super().__init__(program, iterations)

    def run(self):
        self.setLastValue(LEDState(self._maxValue,self._minValue,self._minValue, 1.0))
        LoopedProgram.run(self)
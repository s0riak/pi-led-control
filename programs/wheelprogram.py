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
from ledstate import LEDState
from programs.loopedprogram import LoopedProgram
from programs.colorpathprogram import ColorPathProgram
class WheelProgram(LoopedProgram):

    def __init__(self, printInfo, interations, minValue, maxValue):
        minValue = min(1.0, max(0.0, minValue))
        maxValue = min(1.0, max(0.0, maxValue))
        colorPath = [LEDState(maxValue,minValue,minValue),LEDState(minValue,maxValue,minValue),LEDState(minValue, minValue, maxValue)]
        program = ColorPathProgram(printInfo, colorPath, 50, 0.1)
        
        super().__init__(printInfo, program)

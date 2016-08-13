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
from programs.colorpathprogram import ColorPathProgram
class SunriseProgram(ColorPathProgram):

    def __init__(self, printInfo, duration):
        colorPath = [
            LEDState(0.0,0.0,0.0),
            LEDState(0.0,0.0,0.2),
            LEDState(0.5,0.5,0.2),
            LEDState(1.0,0.9,0.2),
        ]
        interpolationPoints = 60
        timePerColor = duration/((len(colorPath)-1)*interpolationPoints)
        super().__init__(printInfo, colorPath, interpolationPoints, timePerColor)

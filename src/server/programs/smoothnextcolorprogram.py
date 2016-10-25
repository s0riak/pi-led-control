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

from server.programs.colorpathprogram import ColorPathProgram
from server.programs.programchainprogram import ProgramChainProgram
from server.programs.singlecolorprogram import SingleColorProgram
class SmoothNextColorProgram(ProgramChainProgram):

    def __init__(self, ledValue, switchTime):
        colorPath = [ledValue]
        interpolationPoints = 50
        timePerColor =  switchTime/interpolationPoints
        self._colorPathProgram = ColorPathProgram(colorPath, interpolationPoints, timePerColor, True)
        super().__init__([self._colorPathProgram, SingleColorProgram(ledValue)])

    #overridding setLastColor to change duration of softoff based on hue of last Color
    def setLastColor(self, lastColor):
        if lastColor != None:
            lastHue = lastColor[0] + lastColor[1] + lastColor[2]
            totalTime = min(8, max(2, 8 * lastHue / (255*3)))
        else:
            totalTime= 1
        self._colorPathProgram.setTimePerColor(totalTime/50)
        super().setLastColor(lastColor)


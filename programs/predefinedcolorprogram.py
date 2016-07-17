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

from programs.abstractprogram import AbstractProgram
class PredefinedColorProgram(AbstractProgram):

    definedColors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "violet": (148, 0, 211),
        "orange": (255, 165, 0),
        "darkorange": (255, 143, 15),
        "pink": (252, 0, 151),
        "turquoise": (64, 224, 208),
    }
    
    def __init__(self, printInfo, colorName):
        super().__init__(printInfo)
        self._colorName = colorName

    def run(self):
        if self._colorName in self.definedColors.keys():
            color = self.definedColors[self._colorName]
            self._setColorRGB(color[0], color[1], color[2])
        else:
            if self._printInfo:
                print("no predefined color")

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
from programs.abstractprogram import AbstractProgram
class PredefinedColorProgram(AbstractProgram):

    definedColors = {
        "red": LEDState(1.0, 0.0, 0.0),
        "green": LEDState(0.0, 1.0, 0.0),
        "blue": LEDState(0.0, 0.0, 1.0),
        "yellow": LEDState(1.0, 1.0, 0.0),
        "violet": LEDState(0.58, 0.0, 0.82),
        "orange": LEDState(1.0, 0.65, 0.0),
        "darkorange": LEDState(1.0, 0.56, 0.06),
        "pink": LEDState(0.99, 0.0, 0.59),
        "turquoise": LEDState(0.25, 0.88, 0.42),
    }

    @classmethod
    def getPredefinedColorsAsDict(cls):
        result = {}
        for key, value in cls.definedColors.items():
            result[key] = (value.red, value.green, value.blue)
        return result
    
    def __init__(self, printInfo, colorName):
        super().__init__(printInfo)
        self._colorName = colorName

    def run(self):
        if self._colorName in self.definedColors.keys():
            color = self.definedColors[self._colorName]
            self._setValue(color)
        else:
            if self._printInfo:
                print("no predefined color")

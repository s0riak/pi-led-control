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

from server.programs.programchainprogram import ProgramChainProgram
from server.programs.singlecolorprogram import SingleColorProgram
from server.programs.waitprogram import WaitProgram


class DemoProgram(ProgramChainProgram):

    def __init__(self, printInfo, timePerColor=3):
        programs = []
        programs.append(SingleColorProgram(False, 255, 0, 0))
        programs.append(WaitProgram(False, timePerColor))
        programs.append(SingleColorProgram(False, 0, 255, 0))
        programs.append(WaitProgram(False, timePerColor))
        programs.append(SingleColorProgram(False, 0, 0, 255))
        programs.append(WaitProgram(False, timePerColor))
        programs.append(SingleColorProgram(False, 0, 0, 0))
        super().__init__(printInfo, programs)

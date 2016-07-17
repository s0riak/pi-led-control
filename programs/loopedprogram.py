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
class LoopedProgram(AbstractProgram):

    def __init__(self, printInfo, program, iterations=0):
        super().__init__(printInfo)
        self._program = program
        self._iterations = iterations

    def run(self):
        if self._iterations == 0:
            curIter = 0
            while True:
                if self.printInfo:
                    print("current iteration: " + str(curIter))
                self._program.run()
        else:
            for i in range(0, self._iterations):
                if self.printInfo:
                    print("current iteration: " + str(i))
                self._program.run()

    def setThreadStopEvent(self, threadStopEvent):
        self._program.setThreadStopEvent(threadStopEvent)
    
    def getCurrentColor(self):
        return self._program.getCurrentColor()

    def setLastColor(self, lastColor):
        self._program.setLastColor(lastColor)

    def setColorSetter(self, colorSetter):
        self._colorSetter = colorSetter
        self._program.setColorSetter(colorSetter)


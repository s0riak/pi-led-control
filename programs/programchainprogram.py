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
class ProgramChainProgram(AbstractProgram):

    def __init__(self, printInfo, programs):
        super().__init__(printInfo)
        assert len(programs) >= 1
        self._programs = programs
        self._currentProgram = None

    def run(self):        
        self._currentProgram = self._programs[0]
        self._currentProgram.run()
        for program in self._programs[1:]:
            program.setLastValue(self._currentProgram.getCurrentValue())
            self._currentProgram = program
            program.run()
        
    def setThreadStopEvent(self, threadStopEvent):
        self.threadStopEvent = threadStopEvent 
        for program in self._programs:
            program.setThreadStopEvent(threadStopEvent)
    
    def setColorSetter(self, colorSetter):
        self._colorSetter = colorSetter
        for program in self._programs:
            program.setColorSetter(colorSetter)

            
    def getCurrentValue(self):
        return self._currentProgram.getCurrentValue()

    def setLastValue(self, lastValue):
        self._programs[0].setLastValue(lastValue)



# Copyright (c) 2016 Sebastian Kanis
# this file is part of pi-led-control.

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

from abc import ABC, abstractmethod
import traceback
from interruptionexception import InterruptionException
from colorsetter import ColorSetter
class AbstractProgram(ABC):

    def __init__(self, printInfo):
        self.threadStopEvent = None
        self.printInfo = printInfo
        self._lastValue = None
        self._colorSetter = None

    #needs to be called before run
    def setColorSetter(self, colorSetter):
        self._colorSetter = colorSetter
                
    def _setValue(self, value):
        self._colorSetter.setValue(value)

    def getCurrentValue(self):
        if self._colorSetter != None:
            return self._colorSetter.getCurrentValue()
        else:
            return None

    def setLastValue(self, lastValue):
        self._lastValue = lastValue
        
    @abstractmethod
    def run(self):
        raise NotImplementedError

    def setThreadStopEvent(self, threadStopEvent):
        self.threadStopEvent = threadStopEvent
        
    def _waitIfNotStopped(self, time):
        assert self.threadStopEvent != None            
        if self.threadStopEvent.is_set():
            raise InterruptionException
        self.threadStopEvent.wait(time)
        if self.threadStopEvent.is_set():
            raise InterruptionException

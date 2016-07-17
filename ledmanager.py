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

import time
import random
from random import randint

from threading import Thread
from threading import Event
from threading import Semaphore

from ledcontrolthread import LEDControlThread
from colorsetter import ColorSetter

from programs.softoffprogram import SoftOffProgram
class LEDManager():
    

    def __init__(self, printInfo):
        self.printInfo = printInfo
        self.threadStopEvent = Event()
        self.sem = Semaphore()
        self.controlThread = None
        self._cancelPowerOffEvent = None
        self._colorSetter = ColorSetter(printInfo, 1)

    def setBrightness(self, brightness):
        self._colorSetter.setBrightness(brightness)

    def getBrightness(self):
        return self._colorSetter.getBrightness()
    
    def startProgram(self, program):
        self.sem.acquire()
        program.setColorSetter(self._colorSetter)
        if self.controlThread != None:
            self.controlThread.threadStopEvent.set()
            lastColor = self.controlThread.program.getCurrentColor()
            program.setLastColor(lastColor)
        self.controlThread = LEDControlThread(program)
        self.controlThread.start()
        self.sem.release()

    def getCurrentColor(self):
        if self.controlThread != None:
            if self.controlThread.program != None:
                return self.controlThread.program.getCurrentColor()
        return None

    def powerOffWaiter(self,duration, cancelEvent):
        cancelEvent.wait(duration)
        if cancelEvent.is_set():
            if self.printInfo:
                print("canceled power off")
            return
        if self.printInfo:
            print("wait finished starting SoftOffProgram")
        self.startProgram(SoftOffProgram(False))
        self._cancelPowerOffEvent = None
        
    def schedulePowerOff(self, duration):
        if self._cancelPowerOffEvent != None:
            self._cancelPowerOffEvent.set()
        self._cancelPowerOffEvent = Event()
        t = Thread(target=self.powerOffWaiter, args=(duration, self._cancelPowerOffEvent))
        t.start()

    def cancelPowerOff(self):
        if self._cancelPowerOffEvent != None:
            self._cancelPowerOffEvent.set()
            self._cancelPowerOffEvent = None

    def isPowerOffScheduled(self):
        return self._cancelPowerOffEvent != None

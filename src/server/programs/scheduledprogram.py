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

import datetime
import logging

from server.programs.abstractprogram import AbstractProgram


class ScheduledProgram(AbstractProgram):
    def __init__(self, program, timeOfDay):
        super().__init__()
        self._program = program
        self._timeOfDay = timeOfDay

    def run(self):
        now = datetime.datetime.now()
        secondsInCurrentDay = now.hour * 3600 + now.minute * 60 + now.second
        if secondsInCurrentDay < self._timeOfDay:
            sleepDuration = self._timeOfDay - secondsInCurrentDay
        else:
            sleepDuration = self._timeOfDay + 3600 * 24 - secondsInCurrentDay
        logging.getLogger("main").info("sleeping for " + str(sleepDuration) + " seconds")
        self._waitIfNotStopped(sleepDuration)
        self._program.run()

    def setThreadStopEvent(self, threadStopEvent):
        self.threadStopEvent = threadStopEvent
        self._program.setThreadStopEvent(threadStopEvent)

    def setColorSetter(self, colorSetter):
        self._colorSetter = colorSetter
        self._program.setColorSetter(colorSetter)

    def getCurrentColor(self):
        return self._program.getCurrentColor()

    def setLastColor(self, lastColor):
        self._program.setLastColor(lastColor)

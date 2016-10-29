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


import logging
from threading import Event
from threading import Thread

from server.exceptions.interruptionexception import InterruptionException
from server.exceptions.piblasterunavailableexception import PiBlasterUnavailableException
from server.programs.abstractprogram import AbstractProgram


class LEDControlThread(Thread):
  
    def __init__(self, program):
        Thread.__init__(self)
        self.program = program
        self.threadStopEvent = Event()
        
    def run(self):
        assert isinstance(self.program, AbstractProgram)
        try:
            self.program.setThreadStopEvent(self.threadStopEvent)
            self.program.run()
        except InterruptionException:
            logging.getLogger("main").info("killed thread doing " + type(self.program).__name__)
        except PiBlasterUnavailableException as e:
            logging.getLogger("main").error("thread failed doing " + type(self.program).__name__ + ", message: " + str(e))
                
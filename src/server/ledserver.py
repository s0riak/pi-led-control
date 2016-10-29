#!/usr/bin/python3
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

from http.server import HTTPServer
import logging
import os

from server.piledhttprequesthandler import PiLEDHTTPRequestHandler


class LEDServer(HTTPServer):

    def __init__(self, connection, ledManager, configManager):
        self._connection = connection
        self.ledManager = ledManager
        self.config = configManager
        self._serverStarted = False
        super().__init__(connection, PiLEDHTTPRequestHandler)

                
    def serve_forever(self, poll_interval=0.5):
        logging.getLogger("main").info("running %s from %s at %s:%s", __name__, os.path.dirname(os.path.realpath(__file__)), self._connection[0], self._connection[1])
        self._serverStarted = True
        HTTPServer.serve_forever(self, poll_interval=poll_interval)
        
    def server_close(self):
        if self._serverStarted:
            logging.getLogger("main").info("stopping %s, was running from %s at %s:%s", __name__, os.path.dirname(os.path.realpath(__file__)), self._connection[0], self._connection[1])
        HTTPServer.server_close(self)
        if self._serverStarted:
            logging.getLogger("main").info("teardown complete")
        

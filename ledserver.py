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

import argparse
from http.server import HTTPServer
import os
import time

from configmanager import ConfigurationManager
from ledmanager import LEDManager

from piledhttprequesthandler import PiLEDHTTPRequestHandler


class MyServer(HTTPServer):

    def __init__(self, connection, handlerClass, ledManager, configManager):
        super().__init__(connection, PiLEDHTTPRequestHandler)
        self.ledManager = ledManager
        self.config = configManager
                
parser = argparse.ArgumentParser(description='This is the server of pi-led-control')
parser.add_argument('-n', '--name', help='the hostname on which pi-led-control is served', default='')
parser.add_argument('-p', '--port', help='the port on which pi-led-control is served', default=9000)
parser.add_argument('-c', '--configPath', help='the path to the config file to be used', default="pi-led-control.config")
args = vars(parser.parse_args())

myServer = MyServer((args['name'], args['port']), PiLEDHTTPRequestHandler, LEDManager(False), ConfigurationManager(args['configPath']))

try:
    print("running server from {} at {} started on {}:{}".format(os.path.dirname(os.path.realpath(__file__)), time.asctime(), args['name'], args['port']))
    myServer.serve_forever()
except KeyboardInterrupt:
    pass
myServer.server_close()
print("server stopped at {} started on {}:{}".format(time.asctime(), args['name'], args['port']))


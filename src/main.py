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
import logging
import time

from server.configmanager import ConfigurationManager
from server.ledmanager import LEDManager
from server.ledserver import LEDServer
import os

def initLogger(logPath, fileLogLevel, consoleLogLevel):
    logging.getLogger().addHandler(logging.StreamHandler())
    rootLogger = logging.getLogger()
    rootLoggerLevel = min(fileLogLevel, consoleLogLevel)
    rootLogger.setLevel(rootLoggerLevel)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = logging.FileHandler(logPath)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(fileLogLevel)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(consoleLogLevel)
    rootLogger.addHandler(consoleHandler)
    
def main():
    parser = argparse.ArgumentParser(description='This is the server of pi-led-control')
    parser.add_argument('-n', '--name', help='the hostname on which pi-led-control is served', default='')
    parser.add_argument('-p', '--port', help='the port on which pi-led-control is served', default=9000)
    parser.add_argument('-c', '--configPath', help='the path to the config file to be used', default="../pi-led-control.config")
    parser.add_argument('-l', '--logPath', help='the path to the log file to be used', default=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/piledcontrol.log")
    parser.add_argument('-fl', '--fileLogLevel', help='the log level for the logfile', default=logging.INFO)
    parser.add_argument('-cl', '--consoleLogLevel', help='the log level for the console', default=logging.ERROR)
    args = vars(parser.parse_args())

    initLogger(args['logPath'], args['fileLogLevel'], args['consoleLogLevel'])
    ledServer = LEDServer((args['name'], args['port']), LEDManager(), ConfigurationManager(args['configPath']))

    try:
        ledServer.serve_forever()
    except KeyboardInterrupt:
        ledServer.server_close()

if __name__ == '__main__':
    main()
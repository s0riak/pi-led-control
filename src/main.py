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
from logging import handlers
import logging
import os

from server.configmanager import ConfigurationManager
from server.ledmanager import LEDManager
from server.ledserver import LEDServer


def initLogger(loggerName, logPath, fileLogLevel, consoleLogLevel):
    logger = logging.getLogger(loggerName)
    loggerLevel = min(fileLogLevel, consoleLogLevel)
    logger.setLevel(loggerLevel)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = handlers.TimedRotatingFileHandler(logPath, when='D', backupCount=7)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(fileLogLevel)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(consoleLogLevel)
    logger.addHandler(consoleHandler)
    
def main():
    parser = argparse.ArgumentParser(description='This is the server of pi-led-control')
    parser.add_argument('-n', '--name', help='the hostname on which pi-led-control is served', default='')
    parser.add_argument('-p', '--port', help='the port on which pi-led-control is served', type=int, default=9000)
    parser.add_argument('-c', '--configPath', help='the path to the config file to be used', default="../pi-led-control.config")
    logLevelsRange = [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]
    parser.add_argument('-l', '--logPath', help='the path to the log folder to be used', default=os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    parser.add_argument('-fl', '--fileLogLevel', help='the log level for the logfile', type=int, choices=logLevelsRange, default=logging.INFO)
    parser.add_argument('-cl', '--consoleLogLevel', help='the log level for the console', type=int, choices=logLevelsRange, default=logging.ERROR)
    parser.add_argument('-atc', '--accessLogToConsole', help='set to True to print access log entries to console', type=bool, default=False)
    args = vars(parser.parse_args())

    initLogger("main", args['logPath'] + "/piledcontrol.log", args['fileLogLevel'], args['consoleLogLevel'])
    if args['accessLogToConsole']:
        consoleLogLevel = args['consoleLogLevel']
    else:
        consoleLogLevel = logging.CRITICAL
    fileLogLevel = args['fileLogLevel']
    initLogger("access", args['logPath'] + "/piledcontrol_access.log", fileLogLevel, consoleLogLevel)
    logging.getLogger().setLevel(100)
    
    try:
        ledServer = LEDServer((args['name'], args['port']), LEDManager(), ConfigurationManager(args['configPath']))
    except OSError as e:
        if str(e) == "[Errno 98] Address already in use":
            logging.getLogger("main").critical("can't init server, port is already in use")
        else:
            raise e
    else:
        try:
            ledServer.serve_forever()
        except KeyboardInterrupt:
            ledServer.server_close()

if __name__ == '__main__':
    main()
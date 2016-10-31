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

#!/usr/bin/env python3
# This caller relies on https://github.com/50ButtonsEach/fliclib-linux-hci
import json
import requests
import traceback
import logging
from requests.exceptions import HTTPError


class EventHelper():
    
    eventTypes = {"toggleFeed": 0, "toggleWhite": 1, "togglePrograms": 2}
    piLedHost = "http://localhost:9000"   
    
    def __init__(self):
        self._programs = ['randomPath', '4colorloop', 'wheel', 'freak', 'softoff']
        self._programIndex = 0
        
    def isColorValid(self, color):
        if not type(color) == dict:
            return False
        requiredKeys = ["red", "green", "blue"]
        for requiredKey in requiredKeys:
            if not requiredKey in color:
                return False
            elif type(color[requiredKey]) != float:
                return False
            elif float(color[requiredKey]) > 1.0 or float(color[requiredKey]) < 0.0:
                return False
        return True

    def getCurrentColor(self):
        try:
            statusRequestResult = requests.get(EventHelper.piLedHost + "/getStatus")
        except (ConnectionError, HTTPError) as e:
            logging.getLogger("flicintegration").error("getStatus failed with error " + str(e))
            raise e
        return json.loads(statusRequestResult.text)["color"]

    def getFeedRed(self):
        try:
            configurationRequestResult = requests.get(EventHelper.piLedHost + "/getConfiguration")
        except (ConnectionError, HTTPError) as e:
            logging.getLogger("flicintegration").error("getConfiguration failed with error " + str(e))
            raise e
        configurationJsonBody = json.loads(configurationRequestResult.text)
        return configurationJsonBody["programs"]["feed"]["brightness"]
    
    def isFeedProgramActive(self):
        statusColor = self.getCurrentColor()
        if not self.isColorValid(statusColor):
            return False
        configurationRed = self.getFeedRed()
        if float(statusColor["blue"]) != 0.0:
            return False
        if float(statusColor["green"]) != 0.0:
            return False
        if float(statusColor["red"]) != float(configurationRed):
            return False
        return True

    def isFullWhiteProgramActive(self):
        statusColor = self.getCurrentColor()
        if not self.isColorValid(statusColor):
            return False
        if float(statusColor["blue"]) != 1.0:
            return False
        if float(statusColor["green"]) != 1.0:
            return False
        if float(statusColor["red"]) != 1.0:
            return False
        return True
    
    def startProgram(self, programName):
        try:
            requests.post(EventHelper.piLedHost + "/startProgram", json.dumps({'name': programName, 'params': []}))
            logging.getLogger("flicintegration").info("startProgram for " + programName + "called")
        except (ConnectionError, HTTPError) as e:
            logging.getLogger("flicintegration").error("startProgram " + programName + " failed with error " + str(e))
            raise e
    
    def handleEvent(self, eventType):
        try:
            if eventType == EventHelper.eventTypes["toggleFeed"]:
                self._programIndex = 0
                if self.isFeedProgramActive():
                    self.startProgram("softOff")
                else:
                    self.startProgram("feed")
            elif eventType == EventHelper.eventTypes["toggleWhite"]:
                self._programIndex = 0
                if self.isFullWhiteProgramActive():
                    self.startProgram("softOff")
                else:
                    self.startProgram("white")
                    self.startWhiteProgram()
            elif eventType == EventHelper.eventTypes["togglePrograms"]:
                self.startProgram(self._programs[self._programIndex])
                self._programIndex = (self._programIndex + 1) % len(self._programs)
            else:
                logging.getLogger("flicintegration").error("Unsupported eventType " + str(eventType))
        except:
            logging.getLogger("flicintegration").error("handleEvent for event of type " + str(eventType) + " failed " + traceback.format_exc())

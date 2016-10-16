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
import traceback



import sys
import requests
import json

class EventHelper():
    
    eventTypes = {"toggleFeed": 0, "toggleWhite": 1, "togglePrograms": 2}
    piLedHost = "http://localhost:9000"   
    
    def __init__(self):
        self._programs = ['randomPath', '4colorloop', 'wheel', 'freak', 'softoff']
        self._programIndex = 0

    def getCurrentColor(self):
        statusRequestResult = requests.get(EventHelper.piLedHost + "/getStatus")
        return json.loads(statusRequestResult.text)["color"]

    def getFeedRed(self):
        configurationRequestResult = requests.get(EventHelper.piLedHost + "/getConfiguration")
        configurationJsonBody = json.loads(configurationRequestResult.text)
        return configurationJsonBody["programs"]["feed"]["brightness"]
    
    def isFeedProgramActive(self):
        statusColor = self.getCurrentColor()
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
        if float(statusColor["blue"]) != 1.0:
            return False
        if float(statusColor["green"]) != 1.0:
            return False
        if float(statusColor["red"]) != 1.0:
            return False
        return True

    def startSoftOffProgram(self):
        requests.post(EventHelper.piLedHost + "/startProgram", json.dumps({'name': 'softOff', 'params': []}))
    
    def startFeedProgram(self):
        requests.post(EventHelper.piLedHost + "/startProgram", json.dumps({'name': 'feed', 'params': []}))
    
    def startWhiteProgram(self):
        requests.post(EventHelper.piLedHost + "/startProgram", json.dumps({'name': 'white', 'params': []}))
    
    def startNextProgram(self):
        requests.post(EventHelper.piLedHost + "/startProgram", json.dumps({'name': self._programs[self._programIndex], 'params': []}))
    
    def handleEvent(self, eventType):
        try:
            print(str(eventType))
            if eventType == EventHelper.eventTypes["toggleFeed"]:
                self._programIndex = 0
                if self.isFeedProgramActive():
                    self.startSoftOffProgram()
                else:
                    self.startFeedProgram()
            if eventType == EventHelper.eventTypes["toggleWhite"]:
                self._programIndex = 0
                if self.isFullWhiteProgramActive():
                    self.startSoftOffProgram()
                else:
                    self.startWhiteProgram()
            if eventType == EventHelper.eventTypes["togglePrograms"]:
                self.startNextProgram()
                self._programIndex = (self._programIndex + 1) % len(self._programs)
        except:
                print("toggleFeed failed" + traceback.format_exc())

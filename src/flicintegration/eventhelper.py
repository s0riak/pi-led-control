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

# !/usr/bin/env python3
# This caller relies on https://github.com/50ButtonsEach/fliclib-linux-hci
import json
import logging
import traceback
from json import JSONDecodeError

import requests
from requests.exceptions import HTTPError


def startProgram(programName, params=None):
    if params is None:
        params = []
    try:
        requests.post(EventHelper.piLedHost + "/startProgram", json.dumps({'name': programName, 'params': params}))
        logging.getLogger("flicintegration").info("startProgram for " + programName + " called")
    except (ConnectionError, HTTPError) as e:
        logging.getLogger("flicintegration").error("startProgram " + programName + " failed with error " + str(e))
        raise e


def get_dict_value_from_JSON_webservice(host, path, dict_key_path):
    try:
        webservice_result = requests.get(host + path)
    except (ConnectionError, HTTPError) as e:
        logging.getLogger("flicintegration").error(path + "failed with error " + str(e))
        raise e
    try:
        json_result = json.loads(webservice_result.text)
    except JSONDecodeError as e:
        logging.getLogger("flicintegration").error("result of " + path + " could not be parsed " + str(e))
        raise e
    try:
        current_value = json_result
        for path_part in dict_key_path:
            current_value = current_value[path_part]
        return current_value
    except KeyError as e:
        logging.getLogger("flicintegration").error("result of " + path + " is missing path "
                                                   + str(dict_key_path) + " " + str(e))
        raise e

def isColorValid(color):
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


def isFullWhiteProgramActive():
    statusColor = get_dict_value_from_JSON_webservice(EventHelper.piLedHost, "/getStatus", ["color"])
    if not isColorValid(statusColor):
        return False
    elif float(statusColor["blue"]) != 1.0:
        return False
    elif float(statusColor["green"]) != 1.0:
        return False
    elif float(statusColor["red"]) != 1.0:
        return False
    return True


def isFeedProgramActive():
    statusColor = get_dict_value_from_JSON_webservice(EventHelper.piLedHost, "/getStatus", ["color"])
    if not isColorValid(statusColor):
        return False
    configurationRed = get_dict_value_from_JSON_webservice(EventHelper.piLedHost, "/getConfiguration",
                                                           ["programs", "feed", "brightness"])
    if float(statusColor["blue"]) != 0.0:
        return False
    if float(statusColor["green"]) != 0.0:
        return False
    if float(statusColor["red"]) != float(configurationRed):
        return False
    return True


class EventHelper:
    eventTypes = {"toggleFeed": 0, "toggleWhite": 1, "togglePrograms": 2, "toggleTimer": 3}
    piLedHost = "http://localhost:9000"

    def __init__(self):
        self._programs = ['randomPath', '4colorloop', 'wheel', 'freak', 'softoff']
        self._programIndex = 0

    def handleEvent(self, eventType):
        try:
            if eventType == EventHelper.eventTypes["toggleFeed"]:
                self._programIndex = 0
                if isFeedProgramActive():
                    startProgram("softOff")
                else:
                    startProgram("feed")
            elif eventType == EventHelper.eventTypes["toggleWhite"]:
                self._programIndex = 0
                if isFullWhiteProgramActive():
                    startProgram("softOff")
                else:
                    startProgram("white")
            elif eventType == EventHelper.eventTypes["togglePrograms"]:
                startProgram(self._programs[self._programIndex])
                self._programIndex = (self._programIndex + 1) % len(self._programs)
            elif eventType == EventHelper.eventTypes["toggleTimer"]:
                startProgram("feed")
                startProgram("scheduledOff", {"duration": 600})
            else:
                logging.getLogger("flicintegration").error("Unsupported eventType " + str(eventType))
        except:
            logging.getLogger("flicintegration").error(
                "handleEvent for event of type " + str(eventType) + " failed " + traceback.format_exc())

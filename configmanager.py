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

import json
import os.path
import traceback
from pprint import pprint

#to work correctly configuration key must not contain '/'s and '='s
#paths must be given as key1/key2/key3 in case all levels are dictionaries
#in case a level is an array two modes are supported: integers can be used to access entries at a given index (key1/4/key2, returns the 5th element of the array given by key1), attribute selectors like 'attributeName=attributeValue' can be used to select the entry with attributeValue in the attribute with attributeName 
class ConfigurationManager():
    
    def __init__(self, configPath="config.json"):
        self._configPath = configPath
        
    def loadConfig(self):
        if not os.path.isfile(self._configPath):
            print("no configuration found, writing default")
            self.storeConfig(self._getDefaultConfiguration())
        with open(self._configPath) as configFile:    
            return json.load(configFile)

    def storeConfig(self, config):
        with open(self._configPath, 'w') as configFile:
            json.dump(config, configFile)
            pprint(config)

    def _getDefaultConfiguration(self):
        return {
            "programs":
                {
                    "randomPath": {"timePerColor": 3.0},
                    "feed": {"brightness": 0.05},
                    "freak": {"secondsPerColor": 2.0},
                    "sunrise": {"duration": 300, "timeOfDay": -1, "brightness": 1}
                },
            "userDefinedColors":
            [
                {"name": "red",  "values": {"red": 1.0, "green": 0.0, "blue": 0.0}},
                {"name": "green",  "values": {"red": 0.0, "green": 1.0, "blue": 0.0}},
                {"name": "blue", "values": {"red": 0.0, "green": 0.0, "blue": 1.0}},
                {"name": "yellow", "values": {"red": 1.0, "green": 1.0, "blue": 0.0}},
                {"name": "violet", "values": {"red": 0.58, "green": 0.0, "blue": 0.82}},
                {"name": "orange", "values": {"red": 1.0, "green": 0.65, "blue": 0.0}},
                {"name": "darkorange", "values": {"red": 1.0, "green": 0.56, "blue": 0.06}},
                {"name": "pink", "values": {"red": 0.99, "green": 0.0, "blue": 0.59}},
                {"name": "turquoise", "values": {"red": 0.0, "green": 0.88, "blue": 0.78}}
            ]
        }

    def splitKeyValue(self, pathPart):
        if "[" in pathPart:
            pathPartSplit = pathPart.split("[")
            return pathPartSplit[0], pathPartSplit[1][:-1]

    def convertsToInt(self, variable):
        try:
            int(variable)
            return True
        except ValueError:
            return False
        
    def pathExists(self, path):
        config = self.loadConfig()
        if not path:
            return True
        currentConfig = config
        pathParts = path.split('/')
        for i in range(0, len(pathParts)) :
            pathPart = pathParts[i]
            if isinstance(currentConfig, dict):
                if self.convertsToInt(pathPart):
                    raise KeyError("invalid Path " + path)
                if pathPart in currentConfig:
                    if i == len(pathParts) - 1:
                        return True
                    else:
                        currentConfig = currentConfig[pathPart]
                else:
                    return False;
            else:
                if self.convertsToInt(pathPart):
                    index = int(pathPart)
                    if index < 0:
                        raise IndexError("invalid Path " + path)
                    if index >= len(currentConfig):
                        return False
                    else:
                        if i == len(pathParts) - 1:
                            return True
                        else:
                            currentConfig = currentConfig[index]
                elif '=' in pathPart:
                    attributeName = pathPart.split('=')[0]
                    attributeValue = pathPart.split('=')[1]
                    foundInList = False
                    for value in currentConfig:
                        if attributeName in value:
                            if value[attributeName] == attributeValue:
                                if i == len(pathParts) - 1:
                                    return True
                                else:                                
                                    currentConfig = value
                                foundInList = True
                                break
                    if not foundInList:
                        return False
                else:
                    raise KeyError("invalid Path " + path)
    
    def getValue(self, path):
        config = self.loadConfig()
        if not path:
            return config
        currentConfig = config
        pathParts = path.split('/')
        for i in range(0, len(pathParts)) :
            pathPart = pathParts[i]
            if isinstance(currentConfig, dict):
                if self.convertsToInt(pathPart):
                    raise KeyError("invalid Path " + path)
                if pathPart in currentConfig:
                    if i == len(pathParts) - 1:
                        return currentConfig[pathPart]
                    else:
                        currentConfig = currentConfig[pathPart]
                else:
                    raise KeyError("path doesn't exist, key " + pathPart + " not in dict")
            else:
                if self.convertsToInt(pathPart):
                    index = int(pathPart)
                    if index < 0:
                        raise IndexError("invalid Path " + path)
                    if index >= len(currentConfig):
                        raise KeyError("path doesn't exist, index " + str(index) + "out of range")
                    else:
                        if i == len(pathParts) - 1:
                            return currentConfig[index]
                        else:
                            currentConfig = currentConfig[index]
                elif '=' in pathPart:
                    attributeName = pathPart.split('=')[0]
                    attributeValue = pathPart.split('=')[1]
                    foundInList = False
                    for value in currentConfig:
                        if attributeName in value:
                            if value[attributeName] == attributeValue:
                                if i == len(pathParts) - 1:
                                    return value
                                else:                                
                                    currentConfig = value
                                foundInList = True
                                break
                    if not foundInList:
                        raise KeyError("path doesn't exist, attribute " + attributeName + " with value " + attributeValue + " not in dict")
                else:
                    raise KeyError("invalid Path " + path)
        return config
        
    def getValueOld(self, path):
        config = self.loadConfig()
        currentConfig = config
        for pathPart in path.split('/'):
            if isinstance(currentConfig, dict):
                if pathPart in currentConfig:
                    currentConfig = currentConfig[pathPart]
            else:
                for value in currentConfig:
                    if value["name"] == pathPart:
                        currentConfig = value["values"]
        return currentConfig

    #TODO Fix "Name/Value" "Logic" in Lists
    #expects the key/path to be existent in the configuration
    def setValue(self, path, value):
        print("path " + path + " value " + str(value))
        config = self.loadConfig()
        currentConfig = config
        splitParts = path.split('/')
        try:
            for i in range(0, len(splitParts)):
                pathPart = splitParts[i]
                #print("pathPart: " + pathPart)
                #print("currentConfig: ")
                #pprint(currentConfig)
                if isinstance(currentConfig, dict):
                    if pathPart in currentConfig:
                        if i == len(splitParts) -1:
                            #print(path + " found")
                            currentConfig[pathPart] = value
                        else:
                            currentConfig = currentConfig[pathPart]
                else:
                    foundInList = False
                    for listElem in currentConfig:
                        #print("listElem: " + str(listElem))
                        if listElem["name"] == pathPart:
                            foundInList = True
                            if i == len(splitParts) -1:
                                #print(path + " found")
                                listElem["values"] = value
                            else:
                                currentConfig = listElem["values"]
                    if not foundInList:
                        raise ValueError("path " + path + " not found")
            self.storeConfig(config)
        except:
            print("error storing value")
            traceback.print_exc()

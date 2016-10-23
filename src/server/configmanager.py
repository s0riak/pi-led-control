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
import logging
import os.path
from pprint import pprint


#to work correctly configuration key must not contain '/'s and '='s
#paths must be given as key1/key2/key3 in case all levels are dictionaries
#in case a level is an array two modes are supported: integers can be used to access entries at a given index (key1/4/key2, returns the 5th element of the array given by key1), attribute selectors like 'attributeName=attributeValue' can be used to select the entry with attributeValue in the attribute with attributeName 
class ConfigurationManager():
    
    def __init__(self, configPath="config.json"):
        self._configPath = configPath
        
    def loadConfig(self):
        if not os.path.isfile(self._configPath):
            logging.warning("no configuration found, writing default to " + self._configPath)
            self.storeConfig(self._getDefaultConfiguration())
        with open(self._configPath) as configFile:    
            return json.load(configFile)

    def storeConfig(self, config):
        with open(self._configPath, 'w') as configFile:
            json.dump(config, configFile)

    def _getDefaultConfiguration(self):
        return {
            "programs":
                {
                    "randomPath": {"timePerColor": 3.0},
                    "feed": {"brightness": 0.05},
                    "freak": {"secondsPerColor": 2.0},
                    "wheel": {"minBrightness": 0.0, "maxBrightness": 1.0, "timePerColor": 5.0},
                    "sunrise": {"duration": 300, "timeOfDay": -1, "brightness": 1},
                    "colorloop": {"colors": ["red", "yellow", "green", "blue"], "secondsPerColor": 2.0}
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
        
    def pprint(self):
        pprint(self.loadConfig())
        
    def _traverseAndExecute(self, config, path, leafFunction):
        if not path:
            return leafFunction(config)
        currentConfig = config
        pathParts = path.split('/')
        for i in range(0, len(pathParts)) :
            pathPart = pathParts[i]
            if isinstance(currentConfig, dict):
                if self.convertsToInt(pathPart):
                    raise KeyError("invalid Path " + path)
                if pathPart in currentConfig:
                    if i == len(pathParts) - 1:
                        return leafFunction(currentConfig[pathPart])
                    else:
                        currentConfig = currentConfig[pathPart]
                else:
                    raise KeyError("invalid Path " + path)
            else:
                if self.convertsToInt(pathPart):
                    index = int(pathPart)
                    if index < 0:
                        raise IndexError("invalid Path " + path)
                    if index >= len(currentConfig):
                        raise IndexError("invalid Path " + path)
                    else:
                        if i == len(pathParts) - 1:
                            return leafFunction(currentConfig[index])
                        else:
                            currentConfig = currentConfig[index]
                elif '=' in pathPart:
                    attributeName = pathPart.split('=')[0]
                    attributeValue = pathPart.split('=')[1]
                    foundInList = False
                    for value in currentConfig:
                        if attributeName in value:
                            if str(value[attributeName]) == attributeValue:
                                if i == len(pathParts) - 1:
                                    return leafFunction(value)
                                else:                                
                                    currentConfig = value
                                foundInList = True
                                break
                    if not foundInList:
                        raise KeyError("invalid Path " + path)
                else:
                    raise KeyError("invalid Path " + path)
        
    def pathExists(self, path, config=None):
        if config == None:
            config = self.loadConfig()
        try:
            return self._traverseAndExecute(config, path, lambda x: True)
        except IndexError:
            return False
        except KeyError:
            return False
    
    def getValue(self, path, config=None):
        if config == None:
            config = self.loadConfig()
        return self._traverseAndExecute(config, path, lambda x: x)
    
    def getChildCount(self, path, config=None):
        if config == None:
            config = self.loadConfig()
        return self._traverseAndExecute(config, path, lambda x: len(x))
    
    def setValue(self, path, value, createNewLeafs=False):
        if not self.pathExists(path) and not createNewLeafs:
            raise KeyError("invalid Path " + path)
        if not path:
            config = value
        else:
            config = self.loadConfig()
            pathParts = path.rsplit('/',1)
            if len(pathParts) == 1:
                key = pathParts[0]
                parent = config
            else:
                key = pathParts[1]                
                parentPath = pathParts[0]
                if not self.pathExists(parentPath):
                    raise KeyError("invalid Path " + path)
                parent = self.getValue(parentPath, config)
            if isinstance(parent, dict):
                parent[key] = value
            else:
                if '=' in key:
                    attributeName = key.split('=')[0]
                    attributeValue = key.split('=')[1]
                    foundInArray = False
                    for j in range(0, len(parent)):
                        oldValue = parent[j]
                        if attributeName in oldValue:
                            if oldValue[attributeName] == attributeValue:
                                parent[j] = value
                                foundInArray = True
                    if not foundInArray:
                        if not createNewLeafs:
                            raise KeyError("invalid Path " + path)
                        else:
                            parent.append(value)
                else:
                    if int(key) > len(parent) - 1:
                        if not createNewLeafs:
                            raise KeyError("invalid Path " + path)
                        else:
                            if int(key) != len(parent):
                                raise KeyError("invalid Path " + path)
                            else:
                                parent.append(value)
                    else:
                        parent[int(key)] = value
        self.storeConfig(config)
        
    def removeChild(self, path, childId=None):
        if not self.pathExists(path):
            raise KeyError("invalid Path " + path)
        if not path and childId == None:
            config = {}
        else:
            config = self.loadConfig()
            if not path:
                parent = config
            else:
                parent = self.getValue(path, config)
            if childId == None:
                if isinstance(parent, dict):
                    parent.clear()
                elif isinstance(parent, list):
                    parent[:] = []
                else:
                    raise KeyError("invalid Path " + path + "not a list or dict") 
            else:
                if '=' in childId:
                    if isinstance(parent, dict):
                        raise KeyError("invalid key " + childId + " for array at path " + path)
                    attributeName = childId.split('=')[0]
                    attributeValue = childId.split('=')[1]
                    foundInArray = False
                    for child in parent:
                        if attributeName in child:
                            if child[attributeName] == attributeValue:
                                parent.remove(child)
                                foundInArray = True
                                break
                    if not foundInArray:
                        raise KeyError("invalid child " + childId)
                else:
                    if isinstance(parent, dict):
                        if childId in parent:
                            parent.pop(childId)
                        else:
                            raise KeyError("invalid child " + childId)
                    elif isinstance(parent, list):
                        if self.convertsToInt(childId):
                            if int(childId) > len(parent) - 1:
                                raise KeyError("invalid child " + childId)
                            else:
                                parent.pop(int(childId))
                        else:
                            raise KeyError("invalid child " + childId)
                    else:
                        raise KeyError("path " + path + " doesn't contain dict or list")                               
        self.storeConfig(config)
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
from pprint import pprint

#to work correctly configuration key must not contain '/'s
class ConfigurationManager():
    
    def __init__(self):
        self._configPath = 'config.json'
        
    def loadConfig(self):
        if not os.path.isfile(self._configPath):
            print("no configuration found, writing default")
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
                    "randomPath": {"timePerColor": 3},
                    "feed": {"brightness": 0.05}
                }
        }

    def splitKeyValue(self, pathPart):
        if "[" in pathPart:
            pathPartSplit = pathPart.split("[")
            return pathPartSplit[0], pathPartSplit[1][:-1]
        
    def getValue(self, path):
        config = self.loadConfig()
        print(config)
        currentConfig = config
        for pathPart in path.split('/'):
            if isinstance(currentConfig, dict):
                if pathPart in currentConfig:
                    print(pathPart + " found")
                    currentConfig = currentConfig[pathPart]
            else:
                for value in currentConfig:
                    if value["name"] == pathPart:
                        print(pathPart + " found")
                        currentConfig = value["values"]
        return currentConfig
    
    def setValue(self, path, value):
        config = self.loadConfig()
        path.split('/')
        config = self.loadConfig()
        print(config)
        currentConfig = config
        splitParts = path.split('/')
        for i in range(0, len(splitParts)):
            pathPart = splitParts[i]
            if isinstance(currentConfig, dict):
                if pathPart in currentConfig:
                    print(pathPart + " found")
                    if pathPart == splitParts[-1]:
                        currentConfig[pathPart] = value
                    else:
                        currentConfig = currentConfig[pathPart]
            else:
                for listElem in currentConfig:
                    if listElem["name"] == pathPart:
                        print(pathPart + " found")
                        if pathPart == splitParts[-1]:
                            listElem["values"] = value
                        else:
                            currentConfig = listElem["values"]
        self.storeConfig(config)

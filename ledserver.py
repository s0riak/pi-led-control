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

import os
from http.server import CGIHTTPRequestHandler, HTTPServer
import json
import time
import chardet
from chardet.universaldetector import UniversalDetector

from ledmanager import LEDManager
from configmanager import ConfigurationManager
from ledstate import LEDState
from programs.offprogram import OffProgram
from programs.wheelprogram import WheelProgram
from programs.demoprogram import DemoProgram
from programs.allcolorprogram import AllColorProgram
from programs.randomcolorprogram import RandomColorProgram
from programs.smoothrandomprogram import SmoothRandomProgram
from programs.smoothrandomwalkprogram import SmoothRandomWalkProgram
from programs.singlecolorprogram import SingleColorProgram
from programs.predefinedcolorprogram import PredefinedColorProgram
from programs.colorpathprogram import ColorPathProgram
from programs.sunriseprogram import SunriseProgram
from programs.softoffprogram import SoftOffProgram
from programs.scheduledprogram import ScheduledProgram
from programs.loopedprogram import LoopedProgram
from programs.programchainprogram import ProgramChainProgram
from programs.randompathprogram import RandomPathProgram
from programs.smoothnextcolorprogram import SmoothNextColorProgram

hostName = ""
hostPort = 9000

class MyServer(HTTPServer):

    def __init__(self, connection, handlerClass, ledManager):
        super().__init__(connection, MyHandler)
        self.ledManager = ledManager
        self.config = ConfigurationManager()
        
class MyHandler(CGIHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.basename = os.path.dirname(os.path.realpath(__file__)) + "/../client/"
        self._charEncDetector = UniversalDetector()

    #def log_message(self, format, *args):
    #    return
        
    def setLedManager(ledManager):
        self.ledManager = ledManager
        
    def do_GET(self):
        validClientFiles = ["ledclient.css", "ledclient.js", "bootstrap.min.css", "IcoMoon-Free.ttf"]
        if self.path == "" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open(os.path.dirname(os.path.realpath(__file__)) + "/client/" + "index.html")
            self.wfile.write(bytes(f.read(), 'UTF-8'))
            f.close()
            return
        if self.path[1:] in validClientFiles:
            self.send_response(200)
            self.send_header("Content-type", "text/" + self.path.rsplit('.',1)[1])
            self.end_headers()
            resourcePath = os.path.dirname(os.path.realpath(__file__)) + "/client/" + self.path[1:]
            f = open(resourcePath, 'rb')
            detector = UniversalDetector()
            detector.feed(f.read())
            f.close()
            detector.close()
            encoding = detector.result['encoding']
            if encoding == None:
                f = open(resourcePath, 'rb')
                self.wfile.write(f.read())
                f.close()
            else:
                f = open(resourcePath, 'r')
                self.wfile.write(bytes(f.read(), 'UTF-8'))
                f.close()
            return
        elif self.path.startswith("/getPredefinedColors"):
            result = json.dumps(PredefinedColorProgram.getPredefinedColorsAsDict())
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()            
            self.wfile.write(bytes(result, "utf-8"))
        elif self.path.startswith("/getConfiguration"):
            result = json.dumps(self.server.config.getValue(""))
            print(result)
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()            
            self.wfile.write(bytes(result, "utf-8"))
        elif self.path.startswith("/getStatus"):
            resultDict = {}
            resultDict["powerOffScheduled"] = self.server.ledManager.isPowerOffScheduled()
            value = self.server.ledManager.getCurrentValue()
            if not value == None and value.isComplete():
                    resultDict["color"] = {"red": value.red, "green": value.green, "blue": value.blue}
                    resultDict["brightness"] = value.brightness
            else:
                resultDict["brightness"] = None
                resultDict["color"] = None
            result = json.dumps(resultDict)
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()            
            self.wfile.write(bytes(result, "utf-8"))
                

    def getParamsFromJson(self, json, result):
        if not "params" in json:
            print("missing params")
            #TODO errorhandling        
        #print(result.values())
        for key, value in result.items():
            if key in json["params"]:
                if type(value) is int:
                    try:
                        result[key] = int(json["params"][key])
                    except ValueError:
                        print("int expected for key " + key)
                        #TODO correct errorhandling
                elif type(value) is float:
                    try:
                        result[key] = float(json["params"][key])
                    except ValueError:
                        print("float expected for key " + key)
                        #TODO correct errorhandling
                else:
                    result[key] = json["params"][key]
        return result
    
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        requestBody = self.rfile.read(content_len)
        jsonBody = json.loads(requestBody.decode("utf-8"))
        if self.path == "/setBrightness":
            params = {"brightness": 0.0}
            params  = self.getParamsFromJson(jsonBody, params)
            print(params["brightness"])
            self.server.ledManager.setBrightness(params["brightness"])
            self.send_response(200)
            self.end_headers()
        if self.path == "/startProgram":
            if not "name" in jsonBody:
                self.send_response(400)
                self.end_headers()
                return
            progName = jsonBody["name"]
            if progName == "wheel":
                params = {"iterations": 0, "minValue": 0.0, "maxValue": 1.0}
                params  = self.getParamsFromJson(jsonBody, params)
                self.server.ledManager.startProgram(WheelProgram(False, params["iterations"], params["minValue"], params["maxValue"]))
                self.send_response(200)
                self.end_headers()
            elif progName == "sunrise":
                params = {"duration": self.server.config.getValue("programs/sunrise/duration"), "timeOfDay": -1, "brightness": 1.0}
                params  = self.getParamsFromJson(jsonBody, params)
                self.server.config.setValue("programs/sunrise/duration", params["duration"])                
                self.server.config.setValue("programs/sunrise/timeOfDay", params["timeOfDay"])
                self.server.config.setValue("programs/sunrise/brightness", params["brightness"])
                if params["timeOfDay"] == -1:
                    self.server.ledManager.setBrightness(params["brightness"])
                    self.server.ledManager.startProgram(SunriseProgram(False, params["duration"]))
                else:
                    self.server.ledManager.setBrightness(params["brightness"])
                    self.server.ledManager.startProgram(ScheduledProgram(False, SunriseProgram(False, params["duration"]), params["timeOfDay"]))
                self.send_response(200)
                self.end_headers()
            elif progName == "freak":
                params = {"minColor": 0, "maxColor": 1, "secondsPerColor": self.server.config.getValue("programs/freak/secondsPerColor")}
                params  = self.getParamsFromJson(jsonBody, params)
                self.server.ledManager.startProgram(LoopedProgram(False, RandomColorProgram(False, params["minColor"], params["maxColor"], params["secondsPerColor"])))
                self.send_response(200)
                self.end_headers()
            elif progName == "predefined":
                params = {"colorName": ""}
                params  = self.getParamsFromJson(jsonBody, params)
                colors = ""
                for key, value in PredefinedColorProgram.definedColors.items() :
                    if colors == "":
                        colors = key
                    else:
                        colors = colors + ", " + key
                if not params["colorName"] in PredefinedColorProgram.definedColors.keys():
                    self.send_response(400, params["colorName"] + " not in " + colors)
                else:
                    self.server.ledManager.startProgram(PredefinedColorProgram(False, params["colorName"]))
                    self.send_response(200)
                self.end_headers()
            elif progName == "single":
                params = {"red": 0.0, "green": 0.0, "blue": 0.0}
                params  = self.getParamsFromJson(jsonBody, params)
                if not 0 <= params["red"] <= 255 or not 0 <= params["green"] <= 255 or not 0 <= params["blue"] <= 255:
                    self.send_response(400, "invalid values red: {}, green: {}, blue: {}".format(params["red"], params["green"], params["blue"]))
                else:
                    red = params["red"]/255
                    green = params["green"]/255
                    blue = params["blue"]/255
                    self.server.ledManager.startProgram(SingleColorProgram(False, LEDState(red, green, blue, self.server.ledManager.getBrightness())))
                    self.send_response(200)
                self.end_headers()
            elif progName == "softOff":
                self.server.ledManager.startProgram(SoftOffProgram(False))
                self.send_response(200)
                self.end_headers()
            elif progName == "off":
                self.server.ledManager.startProgram(OffProgram(False))
                self.send_response(200)
                self.end_headers()
            elif progName == "4colorloop":
                self.server.ledManager.startProgram(LoopedProgram(False, ColorPathProgram(False, [PredefinedColorProgram.definedColors["blue"],PredefinedColorProgram.definedColors["red"],PredefinedColorProgram.definedColors["yellow"],PredefinedColorProgram.definedColors["green"]], 1, 1), 0))
                self.send_response(200)
                self.end_headers()
            elif progName == "white":
                self.server.ledManager.startProgram(SingleColorProgram(False, LEDState(1.0, 1.0, 1.0, 1.0)))
                self.send_response(200)
                self.end_headers()
            elif progName == "feed":
                self.server.ledManager.startProgram(SmoothNextColorProgram(False, LEDState(self.server.config.getValue("programs/feed/brightness"), 0.0, 0.0, 1.0), 3))
                self.send_response(200)
                self.end_headers()
            elif progName == "randomPath":
                self.server.ledManager.startProgram(RandomPathProgram(False, list(PredefinedColorProgram.definedColors.values()), self.server.config.getValue("programs/randomPath/timePerColor")))
                self.send_response(200)
                self.end_headers()                
            elif progName  == "scheduledOff":
                params = {"duration": 0}
                params  = self.getParamsFromJson(jsonBody, params)
                self.server.ledManager.schedulePowerOff(params["duration"])
                self.send_response(200)
                self.end_headers()                
            elif progName == "cancelScheduledOff":
                self.server.ledManager.cancelPowerOff()
                self.send_response(200)
                self.end_headers()                
            else:
                self.send_response(400)
                self.end_headers()
        if self.path == "/configureProgram":
            if not "name" in jsonBody:
                self.send_response(400)
                self.end_headers()
                return
            progName = jsonBody["name"]
            if progName == "randomPath":
                params = {"timePerColor": self.server.config.getValue("programs/randomPath/timePerColor")}
                params  = self.getParamsFromJson(jsonBody, params)
                self.server.config.setValue("programs/randomPath/timePerColor", params["timePerColor"])
                self.send_response(200)
                self.end_headers()
            elif progName == "feed":
                params = {"brightness": self.server.config.getValue("programs/feed/brightness")}
                params  = self.getParamsFromJson(jsonBody, params)
                print(params)
                self.server.config.setValue("programs/feed/brightness", params["brightness"])
                self.send_response(200)
                self.end_headers()
            elif progName == "freak":
                print("configureFreak")
                params = {"secondsPerColor": self.server.config.getValue("programs/freak/secondsPerColor")}
                print(jsonBody)
                params  = self.getParamsFromJson(jsonBody, params)
                print(params)
                self.server.config.setValue("programs/freak/secondsPerColor", params["secondsPerColor"])
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()



myServer = MyServer((hostName, hostPort), MyHandler, LEDManager(False))
try:
    print("running server from {} at {} started on {}:{}".format(os.path.dirname(os.path.realpath(__file__)), time.asctime(), hostName, hostPort))
    myServer.serve_forever()
except KeyboardInterrupt:
    pass
myServer.server_close()
print("server stopped at {} started on {}:{}".format(time.asctime(), hostName, hostPort))


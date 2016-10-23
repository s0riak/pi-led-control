from chardet.universaldetector import UniversalDetector
from http.server import CGIHTTPRequestHandler
import os
import json
from server.ledstate import LEDState
from server.programs.wheelprogram import WheelProgram
from server.programs.sunriseprogram import SunriseProgram
from server.programs.scheduledprogram import ScheduledProgram
from server.programs.loopedprogram import LoopedProgram
from server.programs.randomcolorprogram import RandomColorProgram
from server.programs.singlecolorprogram import SingleColorProgram
from server.programs.softoffprogram import SoftOffProgram
from server.programs.offprogram import OffProgram
from server.programs.colorpathprogram import ColorPathProgram
from server.programs.smoothnextcolorprogram import SmoothNextColorProgram
from server.programs.randompathprogram import RandomPathProgram
from server.exceptions.parameterexception import ParameterExeption
import traceback
    
class PiLEDHTTPRequestHandler(CGIHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.basename = os.path.dirname(os.path.realpath(__file__)) + "/../client/"
        self._charEncDetector = UniversalDetector()
        self._jsonBody = None

    def setLedManager(self, ledManager):
        self.ledManager = ledManager
        
    def _readFileToBytes(self, requestedPath):
        detector = UniversalDetector()
        with open(requestedPath, 'rb') as f:
            detector.feed(f.read())
            detector.close()
        encoding = detector.result['encoding']
        if encoding == None:
            f = open(requestedPath, 'rb')
            return bytes(f.read())
        else:
            f = open(requestedPath, 'r')
            return bytes(f.read(), encoding)   
         
        
    def _getClientFiles(self, path):
        resourcePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/client/" + path[1:]
        result = self._readFileToBytes(resourcePath)
        self.send_response(200)
        self.send_header("Content-type", "text/" + path.rsplit('.', 1)[1])
        self.end_headers()
        self.wfile.write(result)
        
        
    def _getConfiguration(self):
        result = bytes(json.dumps(self.server.config.getValue("")), "utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(result) 

    def _getStatus(self):
        resultDict = {}
        resultDict["powerOffScheduled"] = self.server.ledManager.isPowerOffScheduled()
        value = self.server.ledManager.getCurrentValue()
        if not value == None and value.isComplete():
            resultDict["color"] = {"red": value.red, "green": value.green, "blue": value.blue}
            resultDict["brightness"] = value.brightness
        else:
            resultDict["brightness"] = None
            resultDict["color"] = None
        result = bytes(json.dumps(resultDict), "utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(result)
        
    def do_GET(self):
        validClientFiles = ["ledclient.css", "ledclient.js", "bootstrap.min.css", "IcoMoon-Free.ttf"]
        try:
            if self.path == "" or self.path == "/" or self.path == "/index.html":
                self._getClientFiles("/index.html")
            elif self.path[1:] in validClientFiles:
                self._getClientFiles(self.path)
            elif self.path == "/getConfiguration":
                self._getConfiguration()
            elif self.path == "/getStatus":
                self._getStatus()
            else:
                self.send_error(404, "invalid path " + self.path)
        except:
            self.send_error(500, "Error processing request for " + self.path, traceback.format_exc())

    def getParamsFromJson(self, result):
        if not "params" in self._jsonBody:
            raise ValueError("missing params in jsonBody")     
        for key, value in result.items():
            if key in self._jsonBody["params"]:
                if type(value) is int:
                    try:
                        result[key] = int(self._jsonBody["params"][key])
                    except ValueError:
                        raise ValueError("int expected for key " + key)
                elif type(value) is float:
                    try:
                        result[key] = float(self._jsonBody["params"][key])
                    except ValueError:
                        raise ValueError("float expected for key " + key)
                else:
                    result[key] = self._jsonBody["params"][key]
        return result
    
    def getPredefinedColor(self, name):
        for color in self.server.config.getValue("userDefinedColors"):
            if color["name"] == name:
                return LEDState(color["values"]["red"], color["values"]["green"], color["values"]["blue"])
        return LEDState(0.0, 0.0, 0.0)

    def getPredefinedColors(self):
        result = []
        for color in self.server.config.getValue("userDefinedColors"):
            result.append(LEDState(color["values"]["red"], color["values"]["green"], color["values"]["blue"]))
        return result

    def loadJSONBody(self):
        content_len = int(self.headers.get('content-length', 0))
        requestBody = self.rfile.read(content_len)
        if requestBody != "":
            self._jsonBody = json.loads(requestBody.decode("utf-8"))
        
    def _setBrightness(self):
        params = {"brightness": 0.0}
        params = self.getParamsFromJson(params)
        self.server.ledManager.setBrightness(params["brightness"])
        self.send_response(200)
        self.end_headers()
        
    def _startWheel(self):
        params = {"iterations": 0, "minValue": self.server.config.getValue("programs/wheel/minBrightness"), "maxValue": self.server.config.getValue("programs/wheel/maxBrightness"), "timePerColor": self.server.config.getValue("programs/wheel/timePerColor")}
        params = self.getParamsFromJson(params)
        self.server.ledManager.startProgram(WheelProgram(False, params["iterations"], params["minValue"], params["maxValue"], params["timePerColor"]))
        
    def _startSunrise(self):
        params = {"duration": self.server.config.getValue("programs/sunrise/duration"), "timeOfDay":-1, "brightness": 1.0}
        params = self.getParamsFromJson(params)
        self.server.config.setValue("programs/sunrise/duration", params["duration"])                
        self.server.config.setValue("programs/sunrise/timeOfDay", params["timeOfDay"])
        self.server.config.setValue("programs/sunrise/brightness", params["brightness"])
        if params["timeOfDay"] == -1:
            self.server.ledManager.setBrightness(params["brightness"])
            self.server.ledManager.startProgram(SunriseProgram(False, params["duration"]))
        else:
            self.server.ledManager.setBrightness(params["brightness"])
            self.server.ledManager.startProgram(ScheduledProgram(False, SunriseProgram(False, params["duration"]), params["timeOfDay"]))
            
    def _startFreak(self):
        params = {"minColor": 0, "maxColor": 1, "secondsPerColor": self.server.config.getValue("programs/freak/secondsPerColor")}
        params = self.getParamsFromJson(params)
        self.server.ledManager.startProgram(LoopedProgram(False, RandomColorProgram(False, params["minColor"], params["maxColor"], params["secondsPerColor"])))
    
    def _startPredefined(self):
        params = {"colorName": ""}
        params = self.getParamsFromJson(params)
        colors = []
        predefinedColors = self.server.config.getValue("userDefinedColors")
        for color in predefinedColors :
            colors.append(color["name"])
        if not params["colorName"] in colors:
            raise ParameterExeption(params["colorName"] + " not in " + str(colors))
        else:
            for predefinedColor in predefinedColors:
                if params["colorName"] == predefinedColor["name"]:
                    color = predefinedColor["values"]
                    ledState = LEDState(color["red"], color["green"], color["blue"], self.server.ledManager.getBrightness())
                    self.server.ledManager.startProgram(SingleColorProgram(False, ledState))
                    break
    
    def _startSingle(self):
        params = {"red": 0.0, "green": 0.0, "blue": 0.0}
        params = self.getParamsFromJson(params)
        if not 0 <= params["red"] <= 255 or not 0 <= params["green"] <= 255 or not 0 <= params["blue"] <= 255:
            raise ParameterExeption("invalid values red: {}, green: {}, blue: {}".format(params["red"], params["green"], params["blue"]))
        else:
            red = params["red"] / 255
            green = params["green"] / 255
            blue = params["blue"] / 255
            self.server.ledManager.startProgram(SingleColorProgram(False, LEDState(red, green, blue, self.server.ledManager.getBrightness())))
    
    def _startColorLoop(self):
        colors = []
        for colorName in self.server.config.getValue("programs/colorloop/colors"):
            colors.append(self.getPredefinedColor(colorName))
            secondsPerColor = self.server.config.getValue("programs/colorloop/secondsPerColor")
            self.server.ledManager.startProgram(LoopedProgram(False, ColorPathProgram(False, colors, 1, secondsPerColor), 0))
            
    def _startScheduledOff(self):
        params = {"duration": 0}
        params = self.getParamsFromJson(params)
        self.server.ledManager.schedulePowerOff(params["duration"])
                
    def _startProgram(self):
        if not "name" in self._jsonBody:
            self.send_response(400, "no program name in request body")
            self.end_headers()
            return
        progName = self._jsonBody["name"]
        try:
            if progName == "wheel":
                self._startWheel()
            elif progName == "sunrise":
                self._startSunrise()
            elif progName == "freak":
                self._startFreak()
            elif progName == "predefined":
                self._startPredefined()
            elif progName == "single":
                self._startSingle()   
            elif progName == "softOff":
                self.server.ledManager.startProgram(SoftOffProgram(False))
            elif progName == "off":
                self.server.ledManager.startProgram(OffProgram(False))
            elif progName == "colorloop":
                self._startColorLoop()
            elif progName == "white":
                self.server.ledManager.startProgram(SingleColorProgram(False, LEDState(1.0, 1.0, 1.0, 1.0)))
            elif progName == "feed":
                self.server.ledManager.startProgram(SmoothNextColorProgram(False, LEDState(self.server.config.getValue("programs/feed/brightness"), 0.0, 0.0, 1.0), 3))
            elif progName == "randomPath":
                self.server.ledManager.startProgram(RandomPathProgram(False, self.getPredefinedColors(), self.server.config.getValue("programs/randomPath/timePerColor")))
            elif progName == "scheduledOff":
                self._startScheduledOff()
            elif progName == "cancelScheduledOff":
                self.server.ledManager.cancelPowerOff()
            else:
                self.send_response(400, "invalid program name " + progName)
                self.end_headers()
            self.send_response(200)
            self.end_headers()
        except ParameterExeption as e:
            self.send_response(400, e)
            self.end_headers()
    
    def _configureRandomPath(self):
        params = {"timePerColor": self.server.config.getValue("programs/randomPath/timePerColor")}
        params = self.getParamsFromJson(params)
        self.server.config.setValue("programs/randomPath/timePerColor", params["timePerColor"])
        
    def _configureFeed(self):
        params = {"brightness": self.server.config.getValue("programs/feed/brightness")}
        params = self.getParamsFromJson(params)
        self.server.config.setValue("programs/feed/brightness", params["brightness"])
        
    def _configureColorLoop(self):
        params = {"colors": self.server.config.getValue("programs/colorloop/colors"), "secondsPerColor": self.server.config.getValue("programs/colorloop/secondsPerColor")}
        params = self.getParamsFromJson(params)
        self.server.config.setValue("programs/colorloop/colors", params["colors"])
        self.server.config.setValue("programs/colorloop/secondsPerColor", params["secondsPerColor"])
        
    def _configureWheel(self):
        params = {"iterations": 0, "minValue": self.server.config.getValue("programs/wheel/minBrightness"), "maxValue": self.server.config.getValue("programs/wheel/maxBrightness"), "timePerColor": self.server.config.getValue("programs/wheel/timePerColor")}
        params = self.getParamsFromJson(params)
        self.server.config.setValue("programs/wheel/minBrightness", params["minValue"])
        self.server.config.setValue("programs/wheel/maxBrightness", params["maxValue"])
        self.server.config.setValue("programs/wheel/timePerColor", params["timePerColor"])
        
    def _configureFreak(self):
        params = {"secondsPerColor": self.server.config.getValue("programs/freak/secondsPerColor")}
        params = self.getParamsFromJson(params)
        self.server.config.setValue("programs/freak/secondsPerColor", params["secondsPerColor"])
            
    def _configureProgram(self):
        if not "name" in self._jsonBody:
            self.send_response(400, "no program name in request body")
            self.end_headers()
            return
        progName = self._jsonBody["name"]
        try:
            if progName == "randomPath":
                self._configureRandomPath()
            elif progName == "feed":
                self._configureFeed()
            elif progName == "colorloop":
                self._configureColorLoop()
            elif progName == "wheel":
                self._configureWheel()
            elif progName == "freak":
                self._configureFreak()
            else:
                self.send_response(400, "invalid program name " + progName)
                self.end_headers()
            self.send_response(200)
            self.end_headers()
        except ParameterExeption as e:
            self.send_response(400, e)
            self.end_headers()
            
    def _configureColor(self):
        params = {"oldName": "", "name": "", "red":-1, "green":-1, "blue":-1}
        params = self.getParamsFromJson(params)
        if params["name"] == "":
            self.send_response(400, "no color name given")             
        elif not 0 <= params["red"] <= 255 or not 0 <= params["green"] <= 255 or not 0 <= params["blue"] <= 255:
            self.send_response(400, "invalid values red: {}, green: {}, blue: {}".format(params["red"], params["green"], params["blue"]))
        else:
            if not self.server.config.pathExists("userDefinedColors/name=" + params["oldName"]):
                colorCount = self.server.config.getChildCount("userDefinedColors")
                self.server.config.setValue("userDefinedColors/" + str(colorCount), {"name" : params["name"], "values": {"red":-1.0, "green":-1.0, "blue":-1.0}}, True)
            else:
                self.server.config.setValue("userDefinedColors/name=" + params["oldName"] + "/name", params["name"])
            self.server.config.setValue("userDefinedColors/name=" + params["name"] + "/values/red", float(params["red"]) / 255)
            self.server.config.setValue("userDefinedColors/name=" + params["name"] + "/values/green", float(params["green"]) / 255)
            self.server.config.setValue("userDefinedColors/name=" + params["name"] + "/values/blue", float(params["blue"]) / 255)
            self.send_response(200)
            self.end_headers()
            
    def _deleteColor(self):
        params = {"name": ""}
        params = self.getParamsFromJson(params)
        if params["name"] == "":
            self.send_response(400, "no color name given")             
        else:
            if not self.server.config.pathExists("userDefinedColors/name=" + params["name"]):
                self.send_response(400, "undefined color given")
            else:
                self.server.config.removeChild("userDefinedColors", "name=" + params["name"])
                self.send_response(200)
                self.end_headers()
    
    def do_POST(self):
        try:
            self.loadJSONBody()
        except:
            self.send_error(400, "Invalid payload for request " + self.path, traceback.format_exc())
            return
        try:
            if self.path == "/setBrightness":
                self._setBrightness()
            elif self.path == "/startProgram":
                self._startProgram()
            elif self.path == "/configureProgram":
                self._configureProgram()
            elif self.path == "/configureColor":
                self._configureColor()
            elif self.path == "/deleteColor":
                self._deleteColor()
            else:
                self.send_error(400, "invalid path")
        except:
            self.send_error(500, "Error processing request for " + self.path, traceback.format_exc())

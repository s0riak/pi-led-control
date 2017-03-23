import inspect
import json
import logging
import os
import traceback
from http.server import CGIHTTPRequestHandler

from chardet.universaldetector import UniversalDetector

from server.exceptions.parameterexception import ParameterExeption
from server.ledstate import LEDState
from server.programs.colorpathprogram import ColorPathProgram
from server.programs.loopedprogram import LoopedProgram
from server.programs.offprogram import OffProgram
from server.programs.randomcolorprogram import RandomColorProgram
from server.programs.randompathprogram import RandomPathProgram
from server.programs.scheduledprogram import ScheduledProgram
from server.programs.singlecolorprogram import SingleColorProgram
from server.programs.smoothnextcolorprogram import SmoothNextColorProgram
from server.programs.sunriseprogram import SunriseProgram
from server.programs.wheelprogram import WheelProgram


def logMethodAndParams(params, logLevel=logging.INFO):
    logging.getLogger("main").log(logLevel, inspect.stack()[1][3] + " with params " + str(params))


def readFileToBytes(requestedPath, encoding):
    if encoding is None:
        f = open(requestedPath, 'rb')
        return bytes(f.read())
    else:
        f = open(requestedPath, 'r')
        return bytes(f.read(), encoding)


def getFileEncoding(filePath):
    detector = UniversalDetector()
    f = open(filePath, 'rb')
    detector.feed(f.read())
    detector.close()
    return detector.result['encoding']


class PiLEDHTTPRequestHandler(CGIHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self._clientResourceBaseDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/client/"
        self._jsonBody = None
        self.ledManager = None
        super().__init__(request, client_address, server)

    def log_error(self, logformat, *args):
        logging.getLogger("access").error("%s - - [%s] %s\n" %
                                          (self.address_string(),
                                           self.log_date_time_string(),
                                           logformat % args))

    def log_request(self, code='-', size='-'):
        # TODO use is_instance instead of try/except
        try:
            # noinspection PyUnresolvedReferences
            code = code.value
        except:
            pass
        logging.getLogger("access").info('"%s" %s %s',
                                         self.requestline, str(code), str(size))

    def setLedManager(self, ledManager):
        self.ledManager = ledManager

    def _getClientFile(self, path):
        resourcePath = self._clientResourceBaseDir + path[1:]
        fileEncoding = getFileEncoding(resourcePath)
        result = readFileToBytes(resourcePath, fileEncoding)
        self.send_response(200)
        if fileEncoding is None:
            self.send_header("Content-type", "application/octet-stream")
        else:
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
        resultDict = {"powerOffScheduled": self.server.ledManager.isPowerOffScheduled()}
        value = self.server.ledManager.getCurrentValue()
        if not value is None and value.isComplete():
            resultDict["color"] = {"red": value.red, "green": value.green, "blue": value.blue}
            resultDict["brightness"] = value.brightness
        else:
            resultDict["brightness"] = None
            resultDict["color"] = None
        result = bytes(json.dumps(resultDict), "utf-8")
        logging.getLogger("main").debug("_getStatus, result: " + json.dumps(resultDict))
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(result)

    def do_GET(self):
        validClientFiles = ["ledclient.css", "ledclient.js", "bootstrap.min.css", "IcoMoon-Free.ttf",
                            "statusWSTest.html", "autobahn.min.js"]
        try:
            if self.path == "" or self.path == "/" or self.path == "/index.html":
                logging.getLogger("main").info("do_GET for index.html")
                self._getClientFile("/index.html")
            elif self.path[1:] in validClientFiles:
                logging.getLogger("main").info("do_GET for " + self.path[1:1])
                self._getClientFile(self.path)
            elif self.path == "/getConfiguration":
                logging.getLogger("main").info("do_GET for getConfiguration")
                self._getConfiguration()
            elif self.path == "/getStatus":
                logging.getLogger("main").debug("do_GET for getStatus")
                self._getStatus()
            else:
                logging.getLogger("main").warning("do_GET called with invalid path " + self.path)
                self.send_error(404, "invalid path " + self.path)
        except:
            logging.getLogger("main").error(
                "Error processing request for " + self.path + "\ntrace: " + traceback.format_exc())
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
        logMethodAndParams(params)
        self.server.ledManager.setBrightness(params["brightness"])
        self.send_response(200)
        self.end_headers()

    def _startWheel(self):
        params = {"iterations": 0, "minValue": self.server.config.getValue("programs/wheel/minBrightness"),
                  "maxValue": self.server.config.getValue("programs/wheel/maxBrightness"),
                  "timePerColor": self.server.config.getValue("programs/wheel/timePerColor")}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        self.server.ledManager.startProgram(
            WheelProgram(params["iterations"], params["minValue"], params["maxValue"], params["timePerColor"]))

    def _startSunrise(self):
        params = {"duration": self.server.config.getValue("programs/sunrise/duration"), "timeOfDay": -1,
                  "brightness": 1.0}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        self.server.config.setValue("programs/sunrise/duration", params["duration"])
        self.server.config.setValue("programs/sunrise/timeOfDay", params["timeOfDay"])
        self.server.config.setValue("programs/sunrise/brightness", params["brightness"])
        if params["timeOfDay"] == -1:
            self.server.ledManager.setBrightness(params["brightness"])
            self.server.ledManager.startProgram(SunriseProgram(params["duration"]))
        else:
            self.server.ledManager.setBrightness(params["brightness"])
            self.server.ledManager.startProgram(
                ScheduledProgram(SunriseProgram(params["duration"]), params["timeOfDay"]))

    def _startFreak(self):
        params = {"minColor": 0, "maxColor": 1,
                  "secondsPerColor": self.server.config.getValue("programs/freak/secondsPerColor")}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        self.server.ledManager.startProgram(
            LoopedProgram(RandomColorProgram(params["minColor"], params["maxColor"], params["secondsPerColor"])))

    def _startPredefined(self):
        params = {"colorName": ""}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        colors = []
        predefinedColors = self.server.config.getValue("userDefinedColors")
        for color in predefinedColors:
            colors.append(color["name"])
        if not params["colorName"] in colors:
            raise ParameterExeption(params["colorName"] + " not in " + str(colors))
        else:
            for predefinedColor in predefinedColors:
                if params["colorName"] == predefinedColor["name"]:
                    color = predefinedColor["values"]
                    ledState = LEDState(color["red"], color["green"], color["blue"],
                                        self.server.ledManager.getBrightness())
                    self.server.ledManager.startProgram(SingleColorProgram(ledState))
                    break

    def _startSingle(self):
        params = {"red": 0.0, "green": 0.0, "blue": 0.0}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        if not 0 <= params["red"] <= 255 or not 0 <= params["green"] <= 255 or not 0 <= params["blue"] <= 255:
            raise ParameterExeption(
                "invalid values red: {}, green: {}, blue: {}".format(params["red"], params["green"], params["blue"]))
        else:
            red = params["red"] / 255
            green = params["green"] / 255
            blue = params["blue"] / 255
            self.server.ledManager.startProgram(
                SingleColorProgram(LEDState(red, green, blue, self.server.ledManager.getBrightness())))

    def _startColorLoop(self):
        logMethodAndParams("")
        colors = []
        for colorName in self.server.config.getValue("programs/colorloop/colors"):
            colors.append(self.getPredefinedColor(colorName))
            secondsPerColor = self.server.config.getValue("programs/colorloop/secondsPerColor")
            self.server.ledManager.startProgram(LoopedProgram(ColorPathProgram(colors, 1, secondsPerColor), 0))

    def _startScheduledOff(self):
        params = {"duration": 0}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
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
                logging.getLogger("main").info(progName)
                self.server.ledManager.startProgram(SmoothNextColorProgram(LEDState(0.0, 0.0, 0.0, 1.0), 1, 3))
            elif progName == "off":
                logging.getLogger("main").info(progName)
                self.server.ledManager.startProgram(OffProgram())
            elif progName == "colorloop":
                self._startColorLoop()
            elif progName == "white":
                logging.getLogger("main").info(progName)
                self.server.ledManager.startProgram(SmoothNextColorProgram(LEDState(1.0, 1.0, 1.0, 1.0), 0.5, 2))
            elif progName == "feed":
                logging.getLogger("main").info(progName)
                self.server.ledManager.startProgram(SmoothNextColorProgram(
                    LEDState(self.server.config.getValue("programs/feed/brightness"), 0.0, 0.0, 1.0), 0.5, 3))
            elif progName == "randomPath":
                logging.getLogger("main").info(progName)
                self.server.ledManager.startProgram(RandomPathProgram(self.getPredefinedColors(),
                                                                      self.server.config.getValue(
                                                                          "programs/randomPath/timePerColor")))
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
        logMethodAndParams(params)
        self.server.config.setValue("programs/randomPath/timePerColor", params["timePerColor"])

    def _configureFeed(self):
        params = {"brightness": self.server.config.getValue("programs/feed/brightness")}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        self.server.config.setValue("programs/feed/brightness", params["brightness"])

    def _configureColorLoop(self):
        params = {"colors": self.server.config.getValue("programs/colorloop/colors"),
                  "secondsPerColor": self.server.config.getValue("programs/colorloop/secondsPerColor")}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        self.server.config.setValue("programs/colorloop/colors", params["colors"])
        self.server.config.setValue("programs/colorloop/secondsPerColor", params["secondsPerColor"])

    def _configureWheel(self):
        params = {"iterations": 0, "minValue": self.server.config.getValue("programs/wheel/minBrightness"),
                  "maxValue": self.server.config.getValue("programs/wheel/maxBrightness"),
                  "timePerColor": self.server.config.getValue("programs/wheel/timePerColor")}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        self.server.config.setValue("programs/wheel/minBrightness", params["minValue"])
        self.server.config.setValue("programs/wheel/maxBrightness", params["maxValue"])
        self.server.config.setValue("programs/wheel/timePerColor", params["timePerColor"])

    def _configureFreak(self):
        params = {"secondsPerColor": self.server.config.getValue("programs/freak/secondsPerColor")}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
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
        params = {"oldName": "", "name": "", "red": -1, "green": -1, "blue": -1}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
        if params["name"] == "":
            self.send_response(400, "no color name given")
        elif not 0 <= params["red"] <= 255 or not 0 <= params["green"] <= 255 or not 0 <= params["blue"] <= 255:
            self.send_response(400, "invalid values red: {}, green: {}, blue: {}".format(params["red"], params["green"],
                                                                                         params["blue"]))
        else:
            if not self.server.config.pathExists("userDefinedColors/name=" + params["oldName"]):
                colorCount = self.server.config.getChildCount("userDefinedColors")
                self.server.config.setValue("userDefinedColors/" + str(colorCount), {"name": params["name"],
                                                                                     "values": {"red": -1.0,
                                                                                                "green": -1.0,
                                                                                                "blue": -1.0}}, True)
            else:
                self.server.config.setValue("userDefinedColors/name=" + params["oldName"] + "/name", params["name"])
            self.server.config.setValue("userDefinedColors/name=" + params["name"] + "/values/red",
                                        float(params["red"]) / 255)
            self.server.config.setValue("userDefinedColors/name=" + params["name"] + "/values/green",
                                        float(params["green"]) / 255)
            self.server.config.setValue("userDefinedColors/name=" + params["name"] + "/values/blue",
                                        float(params["blue"]) / 255)
            self.send_response(200)
            self.end_headers()

    def _deleteColor(self):
        params = {"name": ""}
        params = self.getParamsFromJson(params)
        logMethodAndParams(params)
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
            logging.getLogger("main").warning(
                "Invalid payload for request " + self.path + "\n trace: " + traceback.format_exc())
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
                self.send_error(400, "invalid path " + self.path)
        except:
            self.send_error(500, "Error processing request for " + self.path, traceback.format_exc())

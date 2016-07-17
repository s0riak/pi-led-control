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

import datetime
from ledmanager import LEDManager
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

ledManager = LEDManager(False)
userInput = ""

print(" pi-led-control,\n Copyright (C) 2016 Sebastian Kanis\n pi-led-control comes with ABSOLUTELY NO WARRANTY; for details visit 'https://github.com/s0riak/pi-led-control'. This is free software, and you are welcome to redistribute it under certain conditions; visit 'https://github.com/s0riak/pi-led-control' for details.")
while userInput != "exit":
    userInput = input("Please enter program name to execute or 'exit' to exit:")
    if userInput == "exit":
        ledManager.startProgram(OffProgram(False))
    elif userInput == "wheel":
        ledManager.startProgram(WheelProgram(False, 0, 0, 255))
    elif userInput == "demo":
        ledManager.startProgram(LoopedProgram(False, DemoProgram(False), 4))
    elif userInput == "all":
        ledManager.startProgram(AllColorProgram(False,4, 0.2))
    elif userInput == "freak":
        ledManager.startProgram(LoopedProgram(False, RandomColorProgram(False, 0.2, 1, 0.2)))
    elif userInput == "smooth":
        ledManager.startProgram(SmoothRandomProgram(False, 0.2, 0.2))
    elif userInput == "smoothWalk":
        ledManager.startProgram(SmoothRandomWalkProgram(False, 0.2, 0.2))
    elif userInput == "color":
        userRed = min(255, max(0, int(input("Enter red value (0-255):"))))
        userGreen = min(255, max(0, int(input("Enter green value (0-255):"))))
        userBlue = min(255, max(0, int(input("Enter blue value (0-255):"))))
        ledManager.startProgram(SingleColorProgram(False, userRed, userGreen, userBlue))
    elif userInput == "defined":
        colors = ""
        for key, value in PredefinedColorProgram.definedColors.items() :
            if colors == "":
                colors = key
            else:
                colors = colors + ", " + key
        userColor = input("Enter color name ( " + colors + "):")
        if not userColor in PredefinedColorProgram.definedColors.keys():
            print("invalid color")
        else:
            ledManager.startProgram(PredefinedColorProgram(False, userColor))
    elif userInput == "main":
        ledManager.startProgram(LoopedProgram(False, ColorPathProgram(False, [PredefinedColorProgram.definedColors["blue"],PredefinedColorProgram.definedColors["red"],PredefinedColorProgram.definedColors["yellow"],PredefinedColorProgram.definedColors["green"]], 1, 1), 0))
    elif userInput == "chain":
        ledManager.startProgram(ProgramChainProgram(False, [DemoProgram(False),SoftOffProgram(False), SunriseProgram(False, 30), SoftOffProgram(False), DemoProgram(False), SoftOffProgram(False)]))
    elif userInput == "off":
        ledManager.startProgram(OffProgram(False))
    elif userInput == "white":
        ledManager.startProgram(SingleColorProgram(False, 255, 255, 255))
    elif userInput == "softOff":
        ledManager.startProgram(SoftOffProgram(False))
    elif userInput == "sunrise":
        userDuration = input("Enter duration in seconds:")
        ledManager.startProgram(SunriseProgram(False, min(3600, max(10, int(userDuration)))))
    elif userInput == "randomPath":
        ledManager.startProgram(RandomPathProgram(False, list(PredefinedColorProgram.definedColors.values()), 3))
    elif userInput == "schedulePowerOff":
        powerOffDuration = int(input("Duration in seconds:"))
        ledManager.schedulePowerOff(powerOffDuration)
    elif userInput == "cancelPowerOff":
        ledManager.cancelPowerOff()
    elif userInput == "scheduledSunrise":
        userDuration = input("Enter duration in seconds:")
        now = datetime.datetime.now()
        userStartTime = input("Enter starttime of day as hh:mm:ss (current is: " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "):")
        splittedStartTime = str(userStartTime).split(":")
        if len(splittedStartTime) != 3:
            print("please enter start time as hh:mm:ss")
        else:
            startTime = int(splittedStartTime[0])*3600+int(splittedStartTime[1])*60+int(splittedStartTime[2])
            ledManager.startProgram(ScheduledProgram(True, SunriseProgram(False, min(3600, max(1, int(userDuration)))), startTime))
    else:
        print("please enter one of the following programs ('demo', 'wheel', 'all', 'freak', 'smooth', 'smoothWalk', 'color', 'defined', 'sunrise', 'scheduledSunrise', 'off', 'white', 'softOff', 'randomPath', 'schedulePowerOff', 'cancelPowerOff')")

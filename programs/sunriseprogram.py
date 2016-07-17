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

from programs.colorpathprogram import ColorPathProgram
class SunriseProgram(ColorPathProgram):

    def __init__(self, printInfo, duration):
        colorPath = [
            (0,0,0),
            (0,0,1),
            (0,0,3),
            (0,0,5),
            (2,0,10),
            (5,2,20),
            (10,2,20),
            (20,2,20),
            (30,2,25),
            (40,2,25),
            (50,2,25),
            (60,2,35),
            (80,2,35),
            (100,20,35),
            (120,20,35),
            (130,30,40),
            (140,40,50),
            (150,40,60),
            (160,40,70),
            (170,40,80),
            (180,40,90),
            (190,40,100),
            (200,50,100),
            (200,60,90),
            (200,70,80),
            (200,80,70),
            (200,90,60),
            (200,100,50),
            (200,110,50),
            (200,120,50),
            (200,130,50),
            (210,150,50),
            (220,170,50),
            (230,190,50),
            (240,210,50),
            (250,230,50),
            (255,230,50),
        ]
        interpolationPoints = 60
        timePerColor = duration/((len(colorPath)-1)*interpolationPoints)
        super().__init__(printInfo, colorPath, interpolationPoints, timePerColor)

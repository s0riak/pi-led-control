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
import logging

from server.exceptions.interruptionexception import InterruptionException
from server.ledstate import LEDState
from server.programs.colorpathprogram import ColorPathProgram


class SunriseProgram(ColorPathProgram):
    def __init__(self, duration, sound_file=None):
        self._duration = duration
        self._sound_file = sound_file
        self._sound = None
        colorPath = [
            LEDState(0.0, 0.0, 0.0),
            LEDState(0.0, 0.0, 0.2),
            LEDState(0.5, 0.5, 0.2),
            LEDState(1.0, 0.9, 0.2),
        ]
        interpolationPoints = 60
        timePerColor = duration / ((len(colorPath) - 1) * interpolationPoints)
        super().__init__(colorPath, interpolationPoints, timePerColor)

    def start_sound(self):
        try:
            # TODO but sound initialization to soundmanager to eager load sounds
            import pygame
            pygame.init()
            try:
                self._sound = pygame.mixer.Sound(self._sound_file)
                logging.getLogger("main").warning("sound loaded")
                self._sound.play(loops=-1, fade_ms=int(self._duration * 1000 * 2 / 3))
            except Exception as e:
                logging.getLogger("main").warning(
                    'sound won\'t play because pygame can\'t play the configured file ' + str(e))
        except ImportError as e:
            logging.getLogger("main").warning("sound won't play because pygame is not available " + str(e))

    def stop_sound(self):
        # catch interuption, stop sound and reraise it
        if self._sound is not None:
            logging.getLogger("main").info("stopping sound")
            self._sound.fadeout(1000)

    def run(self):
        if self._sound_file is not None:
            self.start_sound()
            try:
                super().run()
            except InterruptionException as e:
                self.stop_sound()
                raise e
        else:
            super().run()

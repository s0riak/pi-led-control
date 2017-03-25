# Copyright (c) 2016 Sebastian Kanis
# this file is part of pi-led-control.

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

from server.colorfilters.abstractcolorfilter import AbstractColorFilter
from server.ledstate import LEDState


class PolynomialBrightnessFilter(AbstractColorFilter):

    def __init__(self, degree):
        assert(degree > 0.0)
        self._degree = degree
        super().__init__()

    def filter(self, ledstate):
        return LEDState(ledstate.red, ledstate.green, ledstate.blue, ledstate.brightness**self._degree)

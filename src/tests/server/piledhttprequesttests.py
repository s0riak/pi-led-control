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

import sys
from unittest import mock
import unittest
from unittest.mock import patch, MagicMock, call

from server.piledhttprequesthandler import PiLEDHTTPRequestHandler
import traceback


class PiLEDHTTPRequestHandlerTests(unittest.TestCase):
    
    def mock_init(self):
        print("mock_init called")
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.patcher = patch.object(PiLEDHTTPRequestHandler, '__bases__', (mock.MagicMock,))  # @UndefinedVariable
        with self.patcher:
            self.patcher.is_local = True
            self.handler = PiLEDHTTPRequestHandler(None, None, None)
    
    def test_do_GET_IndexCalled(self):
        self.handler.path = "/"
        _getClientFilesMock = MagicMock()
        self.handler._getClientFiles = _getClientFilesMock
        _getConfigurationMock = MagicMock()
        self.handler._getConfiguration = _getConfigurationMock
        _getStatusMock = MagicMock()
        self.handler._getStatus = _getStatusMock
        self.handler.do_GET()
        assert _getClientFilesMock.called
        assert not _getConfigurationMock.called
        assert not _getStatusMock.called
        
    def test_do_GET_getClientFilesCalled(self):
        validClientFiles = ["ledclient.css", "ledclient.js", "bootstrap.min.css", "IcoMoon-Free.ttf"]
        for i in range(0, len(validClientFiles)):
            with self.subTest(i=i):
                self.handler.path = "/" + validClientFiles[i]
                _getClientFilesMock = MagicMock()
                self.handler._getClientFiles = _getClientFilesMock
                _getConfigurationMock = MagicMock()
                self.handler._getConfiguration = _getConfigurationMock
                _getStatusMock = MagicMock()
                self.handler._getStatus = _getStatusMock
                self.handler.do_GET()
                assert _getClientFilesMock.called
                assert not _getConfigurationMock.called
                assert not _getStatusMock.called
                
    def test_do_GET_getConfigurationCalled(self):
        self.handler.path = "/getConfiguration"
        _getClientFilesMock = MagicMock()
        self.handler._getClientFiles = _getClientFilesMock
        _getConfigurationMock = MagicMock()
        self.handler._getConfiguration = _getConfigurationMock
        _getStatusMock = MagicMock()
        self.handler._getStatus = _getStatusMock
        self.handler.do_GET()
        assert not _getClientFilesMock.called
        assert _getConfigurationMock.called
        assert not _getStatusMock.called
        
    def test_do_GET_getStatusCalled(self):
        self.handler.path = "/getStatus"
        _getClientFilesMock = MagicMock()
        self.handler._getClientFiles = _getClientFilesMock
        _getConfigurationMock = MagicMock()
        self.handler._getConfiguration = _getConfigurationMock
        _getStatusMock = MagicMock()
        self.handler._getStatus = _getStatusMock
        self.handler.do_GET()
        assert not _getClientFilesMock.called
        assert not _getConfigurationMock.called
        assert _getStatusMock.called
    
    def test_do_GET_return404OnInvalidPath(self):
        self.handler.path = "/some/non/existing/path"
        _send_errorMock = MagicMock()
        self.handler.send_error = _send_errorMock
        self.handler.do_GET()
        assert _send_errorMock.called
        self.assertEqual(_send_errorMock.call_args, call(404, "invalid path " + self.handler.path))
        
    def test_do_GET_return500OnExceptionRaised(self):
        self.handler.path = "/"
        _getClientFilesMock = MagicMock(side_effect=Exception)
        self.handler._getClientFiles = _getClientFilesMock
        _send_errorMock = MagicMock()
        self.handler.send_error = _send_errorMock
        self.handler.do_GET()
        assert _send_errorMock.called
        self.assertEqual(_send_errorMock.call_args[0][0], 500)
        self.assertEqual(_send_errorMock.call_args[0][1], "Error processing request for " + self.handler.path)
        self.assertNotEqual(_send_errorMock.call_args[0][2], "")
        
    def test_loadJSONBodyExceptionRaisedOnEmptyBody(self):
        _contentLengthMock = MagicMock()
        _contentLengthMock.return_value = 0
        self.handler.headers = MagicMock()
        self.handler.headers.get = _contentLengthMock
        _rFileReadMock = MagicMock()
        _rFileReadMock.return_value = ""
        self.handler.rfile = MagicMock()
        self.handler.rfile.read = _rFileReadMock
        self.assertRaises(Exception,self.handler.loadJSONBody())
        
    def test_do_POST_return400OnInvalidPayload(self):
        self.handler.path = "/"
        _loadJSONBodyMock = MagicMock(side_effect=Exception)
        self.handler.loadJSONBody = _loadJSONBodyMock
        _send_errorMock = MagicMock()
        self.handler.send_error = _send_errorMock
        self.handler.do_POST()
        assert _send_errorMock.called
        self.assertEqual(_send_errorMock.call_args[0][0], 400)
        self.assertEqual(_send_errorMock.call_args[0][1], "Invalid payload for request " + self.handler.path)
        self.assertNotEqual(_send_errorMock.call_args[0][2], "")
        
if __name__ == '__main__':
    unittest.main()
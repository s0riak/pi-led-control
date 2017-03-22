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
import inspect
import os
import unittest
from unittest.mock import patch, MagicMock, call

from server.piledhttprequesthandler import PiLEDHTTPRequestHandler

mock_makeDevBuild = MagicMock()


def mock_init(self, request, client_address, server):
    self._clientResourceBaseDir = os.path.dirname(
        os.path.dirname(os.path.realpath(inspect.getfile(PiLEDHTTPRequestHandler)))) + "/client/"
    self._jsonBody = None
    self.ledManager = None


class PiLEDHTTPRequestHandlerTests(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        with patch('server.piledhttprequesthandler.PiLEDHTTPRequestHandler.__init__', new=mock_init):
            self.handler = PiLEDHTTPRequestHandler(None, None, None)

    def test_getClientFilesValidBinaryFilesReturn200OctetStreamAndContent(self):
        testPath = "/blub"
        testFileContent = bytes("testdata", "UTF-8")
        self.handler._clientResourceBaseDir = "/testBaseDir/"
        getFileEncodingMock = MagicMock()
        getFileEncodingMock.return_value = None
        readFileToBytesMock = MagicMock()
        readFileToBytesMock.return_value = testFileContent
        with patch('server.piledhttprequesthandler.getFileEncoding', new=getFileEncodingMock), \
             patch('server.piledhttprequesthandler.readFileToBytes', new=readFileToBytesMock):
            _sendResponseMock = MagicMock()
            self.handler.send_response = _sendResponseMock
            _sendHeaderMock = MagicMock()
            self.handler.send_header = _sendHeaderMock
            _endHeadersMock = MagicMock()
            self.handler.end_headers = _endHeadersMock
            self.handler.wfile = MagicMock()
            _wFileWriteMock = MagicMock()
            self.handler.wfile.write = _wFileWriteMock
            self.handler._getClientFile(testPath)
            getFileEncodingMock.assert_called_once_with(self.handler._clientResourceBaseDir + testPath[1:])
            readFileToBytesMock.assert_called_once_with(self.handler._clientResourceBaseDir + testPath[1:], None)
            _sendResponseMock.assert_called_once_with(200)
            _sendHeaderMock.assert_called_once_with("Content-type", "application/octet-stream")
            assert _endHeadersMock.called
            _wFileWriteMock.assert_called_with(testFileContent)

    def test_getClientFilesValidTextFilesReturn200ContentTypeBasedOnFileNameAndContent(self):
        testPath = "/blub.css"
        testFileContent = bytes("testdata", "UTF-8")
        self.handler._clientResourceBaseDir = "/testBaseDir/"
        getFileEncodingMock = MagicMock()
        getFileEncodingMock.return_value = "UTF-8"
        readFileToBytesMock = MagicMock()
        readFileToBytesMock.return_value = testFileContent
        with patch('server.piledhttprequesthandler.getFileEncoding', new=getFileEncodingMock), \
             patch('server.piledhttprequesthandler.readFileToBytes', new=readFileToBytesMock):
            _sendResponseMock = MagicMock()
            self.handler.send_response = _sendResponseMock
            _sendHeaderMock = MagicMock()
            self.handler.send_header = _sendHeaderMock
            _endHeadersMock = MagicMock()
            self.handler.end_headers = _endHeadersMock
            self.handler.wfile = MagicMock()
            _wFileWriteMock = MagicMock()
            self.handler.wfile.write = _wFileWriteMock
            self.handler._getClientFile(testPath)
            getFileEncodingMock.assert_called_once_with(self.handler._clientResourceBaseDir + testPath[1:])
            readFileToBytesMock.assert_called_once_with(self.handler._clientResourceBaseDir + testPath[1:], "UTF-8")
            _sendResponseMock.assert_called_once_with(200)
            _sendHeaderMock.assert_called_once_with("Content-type", "text/css")
            assert _endHeadersMock.called
            _wFileWriteMock.assert_called_with(testFileContent)

    def test_getClientFilesPassesExceptionFromGetFileEncoding(self):
        testPath = "/blub.css"
        testFileContent = bytes("testdata", "UTF-8")
        self.handler._clientResourceBaseDir = "/testBaseDir/"
        _getFileEncodingMock = MagicMock(side_effect=IOError)
        self.handler._getFileEncoding = _getFileEncodingMock
        _readFileToBytesMock = MagicMock()
        _readFileToBytesMock.return_value = testFileContent
        self.handler._readFileToBytes = _readFileToBytesMock
        _sendResponseMock = MagicMock()
        self.handler.send_response = _sendResponseMock
        _sendHeaderMock = MagicMock()
        self.handler.send_header = _sendHeaderMock
        _endHeadersMock = MagicMock()
        self.handler.end_headers = _endHeadersMock
        self.handler.wfile = MagicMock()
        _wFileWriteMock = MagicMock()
        self.handler.wfile.write = _wFileWriteMock
        self.assertRaises(IOError, lambda: self.handler._getClientFile(testPath))

    def test_getClientFilesPassesExceptionFromReadFileToBytes(self):
        testPath = "/blub.css"
        testFileContent = bytes("testdata", "UTF-8")
        self.handler._clientResourceBaseDir = "/testBaseDir/"
        _getFileEncodingMock = MagicMock()
        _getFileEncodingMock.return_value = "UTF-8"
        self.handler._getFileEncoding = _getFileEncodingMock
        _readFileToBytesMock = MagicMock(side_effect=IOError)
        _readFileToBytesMock.return_value = testFileContent
        self.handler._readFileToBytes = _readFileToBytesMock
        _sendResponseMock = MagicMock()
        self.handler.send_response = _sendResponseMock
        _sendHeaderMock = MagicMock()
        self.handler.send_header = _sendHeaderMock
        _endHeadersMock = MagicMock()
        self.handler.end_headers = _endHeadersMock
        self.handler.wfile = MagicMock()
        _wFileWriteMock = MagicMock()
        self.handler.wfile.write = _wFileWriteMock
        self.assertRaises(IOError, lambda: self.handler._getClientFile(testPath))

    def test_do_GET_IndexCalled(self):
        self.handler.path = "/"
        _getClientFilesMock = MagicMock()
        self.handler._getClientFile = _getClientFilesMock
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
                self.handler._getClientFile = _getClientFilesMock
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
        self.handler._getClientFile = _getClientFilesMock
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
        self.handler._getClientFile = _getClientFilesMock
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
        self.handler._getClientFile = _getClientFilesMock
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
        self.assertRaises(Exception, self.handler.loadJSONBody())

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

    def test_do_POST_return400OnInvalidPath(self):
        self.handler.path = "/blub"
        _loadJSONBodyMock = MagicMock()
        self.handler.loadJSONBody = _loadJSONBodyMock
        _send_errorMock = MagicMock()
        self.handler.send_error = _send_errorMock
        self.handler.do_POST()
        assert _send_errorMock.called
        self.assertEqual(_send_errorMock.call_args[0][0], 400)
        self.assertEqual(_send_errorMock.call_args[0][1], "invalid path " + self.handler.path)

    def test_do_POST_onlySetBrightnessCalledOnBrightness(self):
        self.handler.path = "/setBrightness"
        _loadJSONBodyMock = MagicMock()
        self.handler.loadJSONBody = _loadJSONBodyMock
        _setBrightnessMock = MagicMock()
        self.handler._setBrightness = _setBrightnessMock
        _startProgramMock = MagicMock()
        self.handler._startProgram = _startProgramMock
        _configureProgramMock = MagicMock()
        self.handler._configureProgram = _configureProgramMock
        _configureColorMock = MagicMock()
        self.handler._configureColor = _configureColorMock
        _deleteColorMock = MagicMock()
        self.handler._deleteColor = _deleteColorMock
        self.handler.do_POST()
        assert _setBrightnessMock.called
        assert not _startProgramMock.called
        assert not _configureProgramMock.called
        assert not _configureColorMock.called
        assert not _deleteColorMock.called

    def test_do_POST_onlyStartProgramCalledOnStartProgram(self):
        self.handler.path = "/startProgram"
        _loadJSONBodyMock = MagicMock()
        self.handler.loadJSONBody = _loadJSONBodyMock
        _setBrightnessMock = MagicMock()
        self.handler._setBrightness = _setBrightnessMock
        _startProgramMock = MagicMock()
        self.handler._startProgram = _startProgramMock
        _configureProgramMock = MagicMock()
        self.handler._configureProgram = _configureProgramMock
        _configureColorMock = MagicMock()
        self.handler._configureColor = _configureColorMock
        _deleteColorMock = MagicMock()
        self.handler._deleteColor = _deleteColorMock
        self.handler.do_POST()
        assert not _setBrightnessMock.called
        assert _startProgramMock.called
        assert not _configureProgramMock.called
        assert not _configureColorMock.called
        assert not _deleteColorMock.called

    def test_do_POST_onlyConfigureProgramCalledOnConfigureProgram(self):
        self.handler.path = "/configureProgram"
        _loadJSONBodyMock = MagicMock()
        self.handler.loadJSONBody = _loadJSONBodyMock
        _setBrightnessMock = MagicMock()
        self.handler._setBrightness = _setBrightnessMock
        _startProgramMock = MagicMock()
        self.handler._startProgram = _startProgramMock
        _configureProgramMock = MagicMock()
        self.handler._configureProgram = _configureProgramMock
        _configureColorMock = MagicMock()
        self.handler._configureColor = _configureColorMock
        _deleteColorMock = MagicMock()
        self.handler._deleteColor = _deleteColorMock
        self.handler.do_POST()
        assert not _setBrightnessMock.called
        assert not _startProgramMock.called
        assert _configureProgramMock.called
        assert not _configureColorMock.called
        assert not _deleteColorMock.called

    def test_do_POST_onlyConfigureColorCalledOnConfigureColor(self):
        self.handler.path = "/configureColor"
        _loadJSONBodyMock = MagicMock()
        self.handler.loadJSONBody = _loadJSONBodyMock
        _setBrightnessMock = MagicMock()
        self.handler._setBrightness = _setBrightnessMock
        _startProgramMock = MagicMock()
        self.handler._startProgram = _startProgramMock
        _configureProgramMock = MagicMock()
        self.handler._configureProgram = _configureProgramMock
        _configureColorMock = MagicMock()
        self.handler._configureColor = _configureColorMock
        _deleteColorMock = MagicMock()
        self.handler._deleteColor = _deleteColorMock
        self.handler.do_POST()
        assert not _setBrightnessMock.called
        assert not _startProgramMock.called
        assert not _configureProgramMock.called
        assert _configureColorMock.called
        assert not _deleteColorMock.called

    def test_do_POST_onlyDeleteColorCalledOnDeleteColor(self):
        self.handler.path = "/deleteColor"
        _loadJSONBodyMock = MagicMock()
        self.handler.loadJSONBody = _loadJSONBodyMock
        _setBrightnessMock = MagicMock()
        self.handler._setBrightness = _setBrightnessMock
        _startProgramMock = MagicMock()
        self.handler._startProgram = _startProgramMock
        _configureProgramMock = MagicMock()
        self.handler._configureProgram = _configureProgramMock
        _configureColorMock = MagicMock()
        self.handler._configureColor = _configureColorMock
        _deleteColorMock = MagicMock()
        self.handler._deleteColor = _deleteColorMock
        self.handler.do_POST()
        assert not _setBrightnessMock.called
        assert not _startProgramMock.called
        assert not _configureProgramMock.called
        assert not _configureColorMock.called
        assert _deleteColorMock.called


if __name__ == '__main__':
    unittest.main()

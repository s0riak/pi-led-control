import unittest

from unittest.mock import patch, MagicMock
import sys
from server.piledhttprequesthandler import PiLEDHTTPRequestHandler
from http.server import CGIHTTPRequestHandler
from unittest import mock
class PiLEDHTTPRequestHandlerTests(unittest.TestCase):
    
    def mock_init(self):
        print("mock_init called")
    
    #@patch("http.server.CGIHTTPRequestHandler")
    #@patch("server.piledhttprequesthandler.PiLEDHTTPRequestHandler.CGIHTTPRequestHandler.__init__", new=mock_init)
    def setUp(self):
        unittest.TestCase.setUp(self)
        patcher = patch.object(PiLEDHTTPRequestHandler, '__bases__', (mock.Mock,))
        with patcher:
            patcher.is_local = True
            self.handler = PiLEDHTTPRequestHandler(None, None, None)
    
    def test_do_GET_IndexCalled(self):
        self.handler.path = "/"
        _getClientFilesMock = MagicMock()
        self.handler._getClientFiles = _getClientFilesMock
        self.handler.do_GET()
        assert _getClientFilesMock.called
        
    
if __name__ == '__main__':
    print(sys.path)
    unittest.main()
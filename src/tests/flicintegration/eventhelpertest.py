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
import requests
import unittest
from unittest.mock import MagicMock

from flicintegration.eventhelper import EventHelper

class EventHelperTest(unittest.TestCase):
    
    def setUp(self):
        self.eventHelper = EventHelper()
        unittest.TestCase.setUp(self)
        
    def test_isFullWhiteProgramActiveIfWhite(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 1.0, "green": 1.0, "blue": 1.0}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        self.assertTrue(self.eventHelper.isFullWhiteProgramActive())
        
    def test_isFullWhiteProgramInActiveIfRed50Percent(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 0.5, "green": 0.0, "blue": 0.0}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        self.assertFalse(self.eventHelper.isFullWhiteProgramActive())
        
    def test_isFullWhiteProgramInActiveIfBlue100Percent(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 0.0, "green": 0.0, "blue": 1.0}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        self.assertFalse(self.eventHelper.isFullWhiteProgramActive())
        
    def test_isFeedProgramActiveIfRedCorrectValue(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 0.5, "green": 0.0, "blue": 0.0}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        getFeedMock = MagicMock()
        getFeedMock.return_value = 0.5
        self.eventHelper.getFeedRed = getFeedMock
        self.assertTrue(self.eventHelper.isFeedProgramActive())
        
    def test_isFeedProgramActiveIfRedInCorrectValue(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 0.5, "green": 0.0, "blue": 0.0}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        getFeedMock = MagicMock()
        getFeedMock.return_value = 0.6
        self.eventHelper.getFeedRed = getFeedMock
        self.assertFalse(self.eventHelper.isFeedProgramActive())
    
    def test_isFeedProgramActiveIfRedCorrectValueButBlue(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 0.5, "green": 0.0, "blue": 0.3}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        getFeedMock = MagicMock()
        getFeedMock.return_value = 0.5
        self.eventHelper.getFeedRed = getFeedMock
        self.assertFalse(self.eventHelper.isFeedProgramActive())
        
    def test_isFeedProgramActiveIfWhite(self):
        getCurrentColorMock = MagicMock()
        getCurrentColorMock.return_value = {"red": 1.0, "green": 1.0, "blue": 1.0}
        self.eventHelper.getCurrentColor = getCurrentColorMock
        getFeedMock = MagicMock()
        getFeedMock.return_value = 1.0
        self.eventHelper.getFeedRed = getFeedMock
        self.assertFalse(self.eventHelper.isFeedProgramActive())
        
    def test_onlyStartFeedOnToggleFeedFromNonFeed(self):
        isFeedProgramActiveMock = MagicMock()
        isFeedProgramActiveMock.return_value = False
        self.eventHelper.isFeedProgramActive = isFeedProgramActiveMock
        startFeedProgramMock = MagicMock()
        self.eventHelper.startFeedProgram = startFeedProgramMock
        startSoftOffProgramMock = MagicMock()
        self.eventHelper.startSoftOffProgram = startSoftOffProgramMock
        startWhiteProgramMock = MagicMock()
        self.eventHelper.startWhiteProgram = startWhiteProgramMock
        startNextProgram = MagicMock()
        self.eventHelper.startNextProgram = startNextProgram
        self.eventHelper.handleEvent(EventHelper.eventTypes["toggleFeed"])
        assert not startSoftOffProgramMock.called
        assert startFeedProgramMock.called
        assert not startWhiteProgramMock.called
        assert not startNextProgram.called
    
    def test_onlyStartSoftOffOnToggleFeedFromFeed(self):
        isFeedProgramActiveMock = MagicMock()
        isFeedProgramActiveMock.return_value = True
        self.eventHelper.isFeedProgramActive = isFeedProgramActiveMock
        startFeedProgramMock = MagicMock()
        self.eventHelper.startFeedProgram = startFeedProgramMock
        startSoftOffProgramMock = MagicMock()
        self.eventHelper.startSoftOffProgram = startSoftOffProgramMock
        startWhiteProgramMock = MagicMock()
        self.eventHelper.startWhiteProgram = startWhiteProgramMock
        startNextProgram = MagicMock()
        self.eventHelper.startNextProgram = startNextProgram
        self.eventHelper.handleEvent(EventHelper.eventTypes["toggleFeed"])
        assert startSoftOffProgramMock.called
        assert not startFeedProgramMock.called
        assert not startWhiteProgramMock.called
        assert not startNextProgram.called
        
    def test_onlyStartSoftOffOnToggleWhiteFromWhite(self):
        isWhiteProgramActiveMock = MagicMock()
        isWhiteProgramActiveMock.return_value = True
        self.eventHelper.isFullWhiteProgramActive = isWhiteProgramActiveMock
        startFeedProgramMock = MagicMock()
        self.eventHelper.startFeedProgram = startFeedProgramMock
        startSoftOffProgramMock = MagicMock()
        self.eventHelper.startSoftOffProgram = startSoftOffProgramMock
        startWhiteProgramMock = MagicMock()
        self.eventHelper.startWhiteProgram = startWhiteProgramMock
        startNextProgram = MagicMock()
        self.eventHelper.startNextProgram = startNextProgram
        self.eventHelper.handleEvent(EventHelper.eventTypes["toggleWhite"])
        assert startSoftOffProgramMock.called
        assert not startFeedProgramMock.called
        assert not startWhiteProgramMock.called
        assert not startNextProgram.called
        
    def test_onlyStartWhiteProgramOnToggleWhiteFromNonWhite(self):
        isWhiteProgramActiveMock = MagicMock()
        isWhiteProgramActiveMock.return_value = False
        self.eventHelper.isFullWhiteProgramActive = isWhiteProgramActiveMock
        startFeedProgramMock = MagicMock()
        self.eventHelper.startFeedProgram = startFeedProgramMock
        startSoftOffProgramMock = MagicMock()
        self.eventHelper.startSoftOffProgram = startSoftOffProgramMock
        startWhiteProgramMock = MagicMock()
        self.eventHelper.startWhiteProgram = startWhiteProgramMock
        startNextProgramMock = MagicMock()
        self.eventHelper.startNextProgram = startNextProgramMock
        self.eventHelper.handleEvent(EventHelper.eventTypes["toggleWhite"])
        assert not startSoftOffProgramMock.called
        assert not startFeedProgramMock.called
        assert startWhiteProgramMock.called
        assert not startNextProgramMock.called
        
    def test_onlyStartNextProgramOnToggleNextProgram(self):
        startFeedProgramMock = MagicMock()
        self.eventHelper.startFeedProgram = startFeedProgramMock
        startSoftOffProgramMock = MagicMock()
        self.eventHelper.startSoftOffProgram = startSoftOffProgramMock
        startWhiteProgramMock = MagicMock()
        self.eventHelper.startWhiteProgram = startWhiteProgramMock
        startNextProgramMock = MagicMock()
        self.eventHelper.startNextProgram = startNextProgramMock
        self.eventHelper.handleEvent(EventHelper.eventTypes["togglePrograms"])
        assert not startSoftOffProgramMock.called
        assert not startFeedProgramMock.called
        assert not startWhiteProgramMock.called
        assert startNextProgramMock.called
        
    def test_startNextProgramOnToggleNextProgramIteratesThroughPrograms(self):
        for i in range(0, len(self.eventHelper._programs) + 1):
            with self.subTest(i=i):
                postMock = MagicMock()
                requests.post = postMock
                self.eventHelper.handleEvent(EventHelper.eventTypes["togglePrograms"])
                postMock.assert_called_once_with(EventHelper.piLedHost + "/startProgram", '{"params": [], "name": "' + self.eventHelper._programs[i%len(self.eventHelper._programs)] + '"}')
        
if __name__ == '__main__':
    unittest.main()
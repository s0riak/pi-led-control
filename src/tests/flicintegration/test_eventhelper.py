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
import logging
import unittest
from json import JSONDecodeError
from unittest.mock import MagicMock, call, patch

import requests
from requests import HTTPError

from flicintegration.eventhelper import EventHelper, isColorValid, isFeedProgramActive, isFullWhiteProgramActive
from tests.testing_helpers import deep_sort


def generate_get_dict_value_from_JSON_webservice_return_value(getStatus, getConfiguration):
    def get_dict_value_from_JSON_webservice_return_value(*args, **kwargs):
        if args[1] == "/getStatus":
            return getStatus
        elif args[1] == "/getConfiguration":
            return getConfiguration
        else:
            raise Exception("invalid call to mock")

    return get_dict_value_from_JSON_webservice_return_value


class EventHelperTest(unittest.TestCase):
    def setUp(self):
        self.eventHelper = EventHelper()
        unittest.TestCase.setUp(self)

    def test_isColorInValidIfNone(self):
        self.assertFalse(isColorValid(None))

    def test_isColorInValidIfEmptyDict(self):
        self.assertFalse(isColorValid({}))

    def test_isColorInvalidIfDictWithMissingRed(self):
        self.assertFalse(isColorValid({"amber": 1.0, "green": 1.0, "blue": 1.0}))

    def test_isColorInvalidIfGreenIsString(self):
        self.assertFalse(isColorValid({"red": 1.0, "green": "full", "blue": 1.0}))

    def test_isColorInvalidIfBlueValueIsOutOfRange(self):
        self.assertFalse(isColorValid({"red": 1.0, "green": 1.0, "blue": 2.5}))

    def test_isColorValidIfCorrectColor(self):
        self.assertTrue(isColorValid({"red": 1.0, "green": 0.5, "blue": 1.0}))

    def test_isFullWhiteProgramActiveIfWhite(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            dict(red=1.0, green=1.0, blue=1.0), 0.5))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertTrue(isFullWhiteProgramActive())

    def test_isFullWhiteProgramInActiveIfRed50Percent(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            dict(red=0.5, green=0.0, blue=0.0), None))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertFalse(isFullWhiteProgramActive())

    def test_isFullWhiteProgramInActiveIfBlue100Percent(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            dict(red=0.0, green=0.0, blue=1.0), None))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertFalse(isFullWhiteProgramActive())

    def test_isFullWhiteProgramInActiveIfColorNone(self):
        isColorValidMock = MagicMock()
        isColorValidMock.return_value = False
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            None, None))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock), \
             patch('flicintegration.eventhelper.isColorValid', new=isColorValidMock):
            self.assertFalse(isFullWhiteProgramActive())

    def test_isFeedProgramActiveIfRedCorrectValue(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            {"red": 0.5, "green": 0.0, "blue": 0.0}, 0.5))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertTrue(isFeedProgramActive())

    def test_isFeedProgramActiveIfRedInCorrectValue(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            {"red": 0.5, "green": 0.0, "blue": 0.0}, 0.6))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertFalse(isFeedProgramActive())

    def test_isFeedProgramActiveIfRedCorrectValueButBlue(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            dict(red=0.5, green=0.0, blue=0.3), 0.5))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertFalse(isFeedProgramActive())

    def test_isFeedProgramInActiveIfColorNone(self):
        isColorValidMock = MagicMock()
        isColorValidMock.return_value = False
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            None, 0.5))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock), \
             patch('flicintegration.eventhelper.isColorValid', new=isColorValidMock):
            self.assertFalse(isFullWhiteProgramActive())

    def test_isFeedProgramActiveIfWhite(self):
        get_dict_value_from_JSON_webservice_mock \
            = MagicMock(side_effect=generate_get_dict_value_from_JSON_webservice_return_value(
            {"red": 1.0, "green": 1.0, "blue": 1.0}, 1.0))
        with patch('flicintegration.eventhelper.get_dict_value_from_JSON_webservice',
                   new=get_dict_value_from_JSON_webservice_mock):
            self.assertFalse(isFeedProgramActive())

    def test_onlyStartFeedOnToggleFeedFromNonFeed(self):
        isFeedProgramActiveMock = MagicMock()
        isFeedProgramActiveMock.return_value = False
        startProgramMock = MagicMock()
        with patch('flicintegration.eventhelper.isFeedProgramActive', new=isFeedProgramActiveMock), \
             patch('flicintegration.eventhelper.startProgram', new=startProgramMock):
            self.eventHelper.handleEvent(EventHelper.eventTypes["toggleFeed"])
        startProgramMock.assert_called_once_with("feed")

    def test_onlyStartSoftOffOnToggleFeedFromFeed(self):
        isFeedProgramActiveMock = MagicMock()
        isFeedProgramActiveMock.return_value = True
        self.eventHelper.isFeedProgramActive = isFeedProgramActiveMock
        startProgramMock = MagicMock()
        with patch('flicintegration.eventhelper.isFeedProgramActive', new=isFeedProgramActiveMock), \
             patch('flicintegration.eventhelper.startProgram', new=startProgramMock):
            self.eventHelper.handleEvent(EventHelper.eventTypes["toggleFeed"])
        startProgramMock.assert_called_once_with("softOff")

    def test_onlyStartSoftOffOnToggleWhiteFromWhite(self):
        isWhiteProgramActiveMock = MagicMock()
        isWhiteProgramActiveMock.return_value = True
        startProgramMock = MagicMock()
        with patch('flicintegration.eventhelper.isFullWhiteProgramActive', new=isWhiteProgramActiveMock), \
             patch('flicintegration.eventhelper.startProgram', new=startProgramMock):
            self.eventHelper.handleEvent(EventHelper.eventTypes["toggleWhite"])
        startProgramMock.assert_called_once_with("softOff")

    def test_onlyStartWhiteProgramOnToggleWhiteFromNonWhite(self):
        isWhiteProgramActiveMock = MagicMock()
        isWhiteProgramActiveMock.return_value = False
        startProgramMock = MagicMock()
        with patch('flicintegration.eventhelper.isFullWhiteProgramActive', new=isWhiteProgramActiveMock), \
             patch('flicintegration.eventhelper.startProgram', new=startProgramMock):
            self.eventHelper.handleEvent(EventHelper.eventTypes["toggleWhite"])
        startProgramMock.assert_called_once_with("white")

    def test_onlyStartNextProgramOnToggleNextProgram(self):
        startProgramMock = MagicMock()
        self.eventHelper._programIndex = 0
        with patch('flicintegration.eventhelper.startProgram', new=startProgramMock):
            self.eventHelper.handleEvent(EventHelper.eventTypes["togglePrograms"])
        startProgramMock.assert_called_once_with(self.eventHelper._programs[0])

    def test_startNextProgramOnToggleNextProgramIteratesThroughPrograms(self):
        for i in range(0, len(self.eventHelper._programs) + 1):
            with self.subTest(i=i):
                post_mock = MagicMock()
                requests.post = post_mock
                self.eventHelper.handleEvent(EventHelper.eventTypes["togglePrograms"])
                # post_mock.assert_any_call()
                call_args = post_mock.call_args
                self.assertEqual(deep_sort(eval(post_mock.call_args[0][1])),
                                 deep_sort({"name": self.eventHelper._programs[ \
                                     i % len(self.eventHelper._programs)], "params": []}))

    def test_startFeedProgramAndScheduledOffProgramOnToggleTimer(self):
        startProgramMock = MagicMock()
        self.eventHelper.startProgram = startProgramMock
        self.eventHelper._programIndex = 0
        with patch('flicintegration.eventhelper.startProgram', new=startProgramMock):
            self.eventHelper.handleEvent(EventHelper.eventTypes["toggleTimer"])
        startProgramMock.assert_has_calls([call("feed"), call("scheduledOff", {"duration": 600})], False)

    def test_startProgramCatchesAndLogsConnectionError(self):
        post_mock = MagicMock(side_effect=ConnectionError)
        requests.post = post_mock
        logger = logging.getLogger('flicintegration')
        with patch.object(logger, 'error') as log_mock:
            from flicintegration import eventhelper
            self.assertRaises(ConnectionError, lambda: eventhelper.startProgram("softOff"))
            self.assertTrue(log_mock.called)

    def test_startProgramCatchesAndLogsHTTPError(self):
        post_mock = MagicMock(side_effect=HTTPError)
        requests.post = post_mock
        logger = logging.getLogger('flicintegration')
        with patch.object(logger, 'error') as log_mock:
            from flicintegration import eventhelper
            self.assertRaises(HTTPError, lambda: eventhelper.startProgram("softOff"))
            self.assertTrue(log_mock.called)

    def test_get_dict_value_from_JSON_webserviceCatchesAndLogsConnectionError(self):
        get_mock = MagicMock(side_effect=ConnectionError)
        requests.get = get_mock
        logger = logging.getLogger('flicintegration')
        with patch.object(logger, 'error') as log_mock:
            from flicintegration import eventhelper
            self.assertRaises(ConnectionError,
                              lambda: eventhelper.get_dict_value_from_JSON_webservice(EventHelper.piLedHost,
                                                                                      "/getConfiguration",
                                                                                      ["programs", "feed",
                                                                                       "brightness"]))
            self.assertTrue(log_mock.called)

    def test_get_dict_value_from_JSON_webserviceCatchesAndLogsHTTPError(self):
        get_mock = MagicMock(side_effect=HTTPError)
        requests.get = get_mock
        logger = logging.getLogger('flicintegration')
        with patch.object(logger, 'error') as log_mock:
            from flicintegration import eventhelper
            self.assertRaises(HTTPError, lambda: eventhelper.get_dict_value_from_JSON_webservice(EventHelper.piLedHost,
                                                                                                 "/getConfiguration",
                                                                                                 ["programs", "feed",
                                                                                                  "brightness"]))
            self.assertTrue(log_mock.called)

    def test_get_dict_value_from_JSON_webserviceExtractCorrectValue(self):
        get_mock = MagicMock()
        return_value = MagicMock()
        return_value.text = "{\"programs\":{\"feed\":{\"brightness\":\"blub\"}}}"
        get_mock.return_value = return_value
        requests.get = get_mock
        from flicintegration import eventhelper
        self.assertEqual(eventhelper.get_dict_value_from_JSON_webservice(EventHelper.piLedHost, "/getConfiguration",
                                                                         ["programs", "feed", "brightness"]), "blub")

    def test_get_dict_value_from_JSON_webserviceCatchesAndLogsJSONException(self):
        get_mock = MagicMock()
        return_value = MagicMock()
        return_value.text = "{\"programs\":{\"feed\":{\"brightness\":\"blub\"}}}"
        get_mock.return_value = return_value
        requests.get = get_mock
        loads_mock = MagicMock()
        loads_mock.side_effect = JSONDecodeError("", "", 0)
        logger = logging.getLogger('flicintegration')
        with patch.object(logger, 'error') as log_mock, patch('json.loads', new=loads_mock):
            from flicintegration import eventhelper
            self.assertRaises(JSONDecodeError,
                              lambda: eventhelper.get_dict_value_from_JSON_webservice(EventHelper.piLedHost,
                                                                                      "/getConfiguration",
                                                                                      ["programs", "feed",
                                                                                       "brightness"]))
            self.assertTrue(log_mock.called)

    def test_get_dict_value_from_JSON_webserviceCatchesAndLogsKeyErrorOnInvalidJSON(self):
        get_mock = MagicMock()
        return_value = MagicMock()
        return_value.text = "{\"programs\":{\"feed\":{\"brighsdftness\":\"blub\"}}}"
        get_mock.return_value = return_value
        requests.get = get_mock
        logger = logging.getLogger('flicintegration')
        with patch.object(logger, 'error') as log_mock:
            from flicintegration import eventhelper
            self.assertRaises(KeyError, lambda: eventhelper.get_dict_value_from_JSON_webservice(EventHelper.piLedHost,
                                                                                                "/getConfiguration",
                                                                                                ["programs", "feed",
                                                                                                 "brightness"]))
            self.assertTrue(log_mock.called)


if __name__ == '__main__':
    unittest.main()

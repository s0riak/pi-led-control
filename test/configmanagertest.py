import os
import shutil
import time
import unittest

from configmanager import ConfigurationManager


class MockedConfigManager(ConfigurationManager):
    
    def _getDefaultConfiguration(self):
        return {
            "dictOfDicts":
                {
                    "name1": {"intAttribute": 42},
                    "name2": {"floatAttribute": 3.5},
                    "name3": {"stringAttribute": "fortytwo"},
                    "sunrise": {"firstAttribute": 73, "secondAttribute": "thirtyseven"}
                },
            "arrayOfDicts":
            [
                {"pivotAttribute": "pivotValue1",  "otherAttribute": 21},
                {"pivotAttribute": "pivotValue2",  "otherAttribute2": "12"},
                {"pivotAttribute": "pivotValue3", "otherAttribute3": {"deepAttribute1": 1001001, "deepAttribute2": "Anagram", "deepAttribute3": None}},
                {"pivotAttribute": "pivotValue4", "otherAttribute3": {"deepAttribute1": 110110, "deepAttribute2": "Anagram", "deepAttribute3": None}},
                {"nonPivotAttribute": "nonPivotValue", "otherAttribute4": "justAnotherValue"}
            ]
        }

class ConfigurationManagerTest(unittest.TestCase):
    
    def setUp(self):
        self.testConfigPath = str(time.time()) + "configManagerTest.config"    
        self.config = MockedConfigManager(self.testConfigPath)
        
    def tearDown(self):
        os.remove(self.testConfigPath)

    def test_emptyPathExits(self):
        self.assertTrue(self.config.pathExists(""))

if __name__ == '__main__':
    unittest.main()
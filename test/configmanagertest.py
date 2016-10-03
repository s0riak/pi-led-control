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
                    "name4": {"firstAttribute": 73, "secondAttribute": "thirtyseven"}
                },
            "arrayOfDicts":
            [
                {"pivotAttribute1": "pivotValue1",  "otherAttribute": 21},
                {"pivotAttribute1": "pivotValue2",  "otherAttribute2": "12"},
                {"pivotAttribute1": "pivotValue3", "otherAttribute3": {"deepAttribute1": 1001001, "deepAttribute2": "Anagram", "deepAttribute3": None}},
                {"pivotAttribute1": "pivotValue4", "otherAttribute3": {"deepAttribute1": 110110, "deepAttribute2": "Anagram", "deepAttribute3": None}},
                {"pivotAttribute2": "pivotValue5", "otherAttribute4": "justAnotherValue"}
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
        
    def test_firstLevelPathExits(self):
        self.assertTrue(self.config.pathExists("dictOfDicts"))
        self.assertTrue(self.config.pathExists("arrayOfDicts"))
        self.assertFalse(self.config.pathExists("abc"))
        
    def test_secondLevelDictPathExists(self):
        self.assertTrue(self.config.pathExists("dictOfDicts/name1"))
        self.assertTrue(self.config.pathExists("dictOfDicts/name2"))
        self.assertTrue(self.config.pathExists("dictOfDicts/name3"))
        self.assertTrue(self.config.pathExists("dictOfDicts/name4"))
        self.assertFalse(self.config.pathExists("dictOfDicts/abc"))
        self.assertFalse(self.config.pathExists("dictOfDicts/name5"))
        with self.assertRaises(KeyError):
            self.config.pathExists("dictOfDicts/42")
        
    def test_secondLevelArrayByIndexPathExists(self):
        self.assertTrue(self.config.pathExists("arrayOfDicts/0"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/1"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/2"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/3"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/4"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/5"))  

        
    def test_secondLevelArrayByAttributePathExists(self):
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue1"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue2"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue3"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue4"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue5"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute2=pivotValue5"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/pivotAttribute2=pivotValue1"))
        
if __name__ == '__main__':
    unittest.main()
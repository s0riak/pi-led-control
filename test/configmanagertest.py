import os
import shutil
import time
import unittest

from configmanager import ConfigurationManager

testData = {
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

testEditData = {"newAttribute1": 42, "newAttribute2": "wow"}

class MockedConfigManager(ConfigurationManager):
    
    def _getDefaultConfiguration(self):
        return testData

class ConfigurationManagerTest(unittest.TestCase):
    
    def setUp(self):
        self.testConfigPath = "configManagerTest_" + str(time.time()) + ".config"    
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
        self.assertFalse(self.config.pathExists("dictOfDicts/42"))
        
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
        
    def test_thirdLevelDictPathExists(self):
        self.assertTrue(self.config.pathExists("dictOfDicts/name4/firstAttribute"))
        self.assertTrue(self.config.pathExists("dictOfDicts/name4/secondAttribute"))
        self.assertFalse(self.config.pathExists("dictOfDicts/name4/thirdAttribute"))
        self.assertFalse(self.config.pathExists("dictOfDicts/name3/firstAttribute"))
        
    def test_thirdLevelArrayByIndexPathExists(self):
        self.assertTrue(self.config.pathExists("arrayOfDicts/2/otherAttribute3/deepAttribute1"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/2/otherAttribute3/deepAttribute2"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/2/otherAttribute3/deepAttribute3"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/2/otherAttribute3/deepAttribute4"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/2/otherAttribute3/abc"))

    def test_thirdLevelArrayByAttributePathExists(self):
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3/deepAttribute1"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3/deepAttribute2"))
        self.assertTrue(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3/deepAttribute3"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3/deepAttribute4"))
        self.assertFalse(self.config.pathExists("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3/abc"))
        
    def test_rootGetValue(self):
        self.assertEqual(self.config.getValue(""), testData)
        
    def test_firstLevelDictGetValue(self):
        self.assertEqual(self.config.getValue("dictOfDicts"), testData["dictOfDicts"])
        self.assertEqual(self.config.getValue("arrayOfDicts"), testData["arrayOfDicts"])
        
    def test_secondLevelDictGetValue(self):
        self.assertEqual(self.config.getValue("dictOfDicts/name1"), testData["dictOfDicts"]["name1"])
        self.assertEqual(self.config.getValue("dictOfDicts/name4"), testData["dictOfDicts"]["name4"])
        
    def test_secondLevelArrayIndexGetValue(self):
        for i in range(0, len(testData["arrayOfDicts"])):
            with self.subTest(i=i):
                self.assertEqual(self.config.getValue("arrayOfDicts/" + str(i)), testData["arrayOfDicts"][i])
        with self.assertRaises(IndexError):
            self.config.getValue("arrayOfDicts/-1")
        with self.assertRaises(IndexError):
            self.config.getValue("arrayOfDicts/20")
    
    def test_secondLevelArrayAttributeGetValue(self):
        self.assertEqual(self.config.getValue("arrayOfDicts/pivotAttribute1=pivotValue3"), testData["arrayOfDicts"][2])
        with self.assertRaises(KeyError):
            self.config.getValue("arrayOfDicts/pivotAttribute1=abc")
        with self.assertRaises(KeyError):
            self.config.getValue("arrayOfDicts/pivotAttribute1=pivotValue5")
        with self.assertRaises(KeyError):
            self.config.getValue("arrayOfDicts/abc=pivotValue3")
    
    def test_rootLevelEditValue(self):
        self.config.setValue("", testEditData)
        self.assertEqual(self.config.getValue(""), testEditData)
    
    def test_firstLevelEditValue(self):
        self.config.setValue("dictOfDicts", testEditData)
        self.assertEqual(self.config.getValue("dictOfDicts"), testEditData)
    
    def test_secondLevelDictEditValue(self):
        self.config.setValue("dictOfDicts/name2", testEditData)
        self.assertEqual(self.config.getValue("dictOfDicts/name2"), testEditData)
    
    def test_secondLevelArrayIndexEditValue(self):
        self.config.setValue("arrayOfDicts/2", testEditData)
        self.assertEqual(self.config.getValue("arrayOfDicts/2"), testEditData)
    
    def test_secondLevelArrayAttributeEditValue(self):
        self.config.setValue("arrayOfDicts/pivotAttribute1=pivotValue3", testEditData)
        self.assertEqual(self.config.getValue("arrayOfDicts/newAttribute1=42"), testEditData)
    
    def test_thirdLevelDictEditValue(self):
        self.config.setValue("dictOfDicts/name4/secondAttribute", testEditData)
        self.assertEqual(self.config.getValue("dictOfDicts/name4/secondAttribute"), testEditData)
    
    def test_thirdLevelArrayIndexEditValue(self):
        self.config.setValue("arrayOfDicts/2/otherAttribute3", testEditData)
        self.assertEqual(self.config.getValue("arrayOfDicts/2/otherAttribute3"), testEditData)
    
    def test_thirdLevelArrayAttributeEditValue(self):
        self.config.setValue("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3", testEditData)
        self.assertEqual(self.config.getValue("arrayOfDicts/pivotAttribute1=pivotValue3/otherAttribute3"), testEditData)
        
    def test_rootLevelAddArray(self):
        self.config.setValue("newArray", [], True)
        self.assertTrue(self.config.pathExists("newArray"))
        self.assertEqual(self.config.getValue("newArray"), [])

    def test_rootLevelAddDict(self):
        self.config.setValue("newDict", {}, True)
        self.assertTrue(self.config.pathExists("newDict"))
        self.assertEqual(self.config.getValue("newDict"), {})
        
    def test_firstLevelAddArrayToArrayByIndex(self):
        self.config.setValue("arrayOfDicts/5", [], True)
        self.assertTrue(self.config.pathExists("arrayOfDicts/5"))
        self.assertEqual(self.config.getValue("arrayOfDicts/5"), [])

    def test_firstLevelAddDictToArrayByAttribute(self):
        newDict = {"newAttributeName": "newAttributeValue"}
        self.config.setValue("arrayOfDicts/newAttributeName=newAttributeValue", newDict, True)
        self.assertTrue(self.config.pathExists("arrayOfDicts/newAttributeName=newAttributeValue"))
        self.assertEqual(self.config.getValue("arrayOfDicts/newAttributeName=newAttributeValue"), newDict)
    
    def test_firstLevelAddArrayToDict(self):
        self.config.setValue("dictOfDicts/newArray", [], True)
        self.assertTrue(self.config.pathExists("dictOfDicts/newArray"))
        self.assertEqual(self.config.getValue("dictOfDicts/newArray"), [])
        
    def test_secondLevelAddArrayToDictInArray(self):
        testPath = "arrayOfDicts/pivotAttribute1=pivotValue2/newAttribute"
        self.config.setValue(testPath, [], True)
        self.assertTrue(self.config.pathExists(testPath))
        self.assertEqual(self.config.getValue(testPath), [])

    def test_multiAddPath(self):
        self.config.setValue("newEntry", [], True)
        self.config.setValue("newEntry/0", {"newAttributeName": "innerAttributeValue"}, True)
        self.config.setValue("newEntry/newAttributeName=innerAttributeValue/newLeafList", [], True)
        self.config.setValue("newEntry/0/newLeafList/0", "value1", True)
        self.config.setValue("newEntry/0/newLeafList/1", "value2", True)
        self.config.setValue("newEntry/newAttributeName=innerAttributeValue/newLeafList/2", "value3", True)
        self.assertTrue(self.config.pathExists("newEntry/0/newLeafList/0"))
        self.assertTrue(self.config.pathExists("newEntry/newAttributeName=innerAttributeValue/newLeafList/1"))
        self.assertTrue(self.config.pathExists("newEntry/0/newLeafList/2"))
        self.assertEqual(self.config.getValue("newEntry/newAttributeName=innerAttributeValue/newLeafList/0"), "value1")
        self.assertEqual(self.config.getValue("newEntry/0/newLeafList/1"), "value2")
        self.assertEqual(self.config.getValue("newEntry/newAttributeName=innerAttributeValue/newLeafList/2"), "value3")    
        
if __name__ == '__main__':
    unittest.main()
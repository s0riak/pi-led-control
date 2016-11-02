import json
import requests
class StatusPublisher():
    
    def __init__(self, server):
        self.server = server
        self._crossbarHost = "http://localhost:9002"
    
    def publishStatus(self):
        resultDict = {}
        resultDict["powerOffScheduled"] = self.server.ledManager.isPowerOffScheduled()
        value = self.server.ledManager.getCurrentValue()
        if not value == None and value.isComplete():
            resultDict["color"] = {"red": value.red, "green": value.green, "blue": value.blue}
            resultDict["brightness"] = value.brightness
        else:
            resultDict["brightness"] = None
            resultDict["color"] = None
        requestBody = json.dumps({"topic": "ledcontrol.status", "kwargs" : resultDict})
        print(self._crossbarHost)
        print(requestBody)
        result = requests.post(self._crossbarHost, requestBody)
        print(result.status_code)

statusPublisherInstance = None

def initStatusPublisher(server):
    global statusPublisherInstance
    statusPublisherInstance = StatusPublisher(server)
    
def getStatusPublisher():
    global statusPublisherInstance
    assert statusPublisherInstance != None
    return statusPublisherInstance
        
if __name__ == '__main__':
    publisher = StatusPublisher(None)
    publisher.publishStatus()
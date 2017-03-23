import json

import requests


class StatusPublisher:
    def __init__(self, server):
        self.server = server
        self._crossbarHost = "http://localhost:9002"

    def publishStatus(self):
        resultDict = {"powerOffScheduled": self.server.ledManager.isPowerOffScheduled()}
        value = self.server.ledManager.getCurrentValue()
        if not value is None and value.isComplete():
            resultDict["color"] = {"red": value.red, "green": value.green, "blue": value.blue}
            resultDict["brightness"] = value.brightness
        else:
            resultDict["brightness"] = None
            resultDict["color"] = None
        requestBody = json.dumps({"topic": "ledcontrol.status", "kwargs": resultDict})
        requests.post(self._crossbarHost, requestBody)


statusPublisherInstance = None


def initStatusPublisher(server):
    global statusPublisherInstance
    statusPublisherInstance = StatusPublisher(server)


def getStatusPublisher():
    global statusPublisherInstance
    assert statusPublisherInstance is not None
    return statusPublisherInstance


if __name__ == '__main__':
    publisher = StatusPublisher(None)
    publisher.publishStatus()

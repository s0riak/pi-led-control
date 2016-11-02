'''
Created on Nov 2, 2016

@author: sebi
'''
import os
import subprocess
import signal
import sys

class CrossbarManager(object):


    def __init__(self, configurationPath):
        self._configurationPath = configurationPath
        self._crossbarProcess = None
        self._crossbarCall = ["crossbar", "start", "--cbdir=" + self._configurationPath]
        
    def start(self):
        self._crossbarProcess = subprocess.Popen(self._crossbarCall)
        
    def stop(self):
        self._crossbarProcess.kill()
        print("crossbar killed")

manager = None
    
def cleanUpAndExit(signal, frame):
    global manager
    print('Cancelled!')
    manager.stop()
    sys.exit(0)
        
def main():
    global manager
    manager = CrossbarManager(os.path.dirname(os.path.realpath(__file__)) + "/crossbar_config")
    manager.start()
    signal.signal(signal.SIGINT, cleanUpAndExit)
    while True:
        pass

if __name__ == '__main__':
    main()
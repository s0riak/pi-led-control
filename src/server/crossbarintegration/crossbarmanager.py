"""
Created on Nov 2, 2016

@author: sebi
"""
import os
import signal
import subprocess
import sys
import time


class CrossbarManager(object):
    def __init__(self, configurationPath):
        self._configurationPath = configurationPath
        self._crossbarProcess = None
        self._crossbarCall = ["crossbar", "start", "--cbdir=" + self._configurationPath]

    def start(self):
        self._crossbarProcess = subprocess.Popen(self._crossbarCall)

    def stop(self):
        if self._crossbarProcess is not None:
            if self._crossbarProcess.returncode is None:
                self._crossbarProcess.terminate()
                if self._crossbarProcess.returncode is None:
                    self._crossbarProcess.kill()
                    if self._crossbarProcess.returncode is not None:
                        print("failed to kill crossbar")
                        return
        print("crossbar killed")


manager = None


def cleanUpAndExit(signal_type, frame):
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
        time.sleep(60)


if __name__ == '__main__':
    main()

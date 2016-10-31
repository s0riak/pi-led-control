#!/usr/bin/env python3
# This caller relies on https://github.com/50ButtonsEach/fliclib-linux-hci
import sys
import traceback


import logging
from logging import handlers
import os
from eventhelper import EventHelper  # @UnresolvedImport

FLIC_LIB_PATH = "/home/pi/fliclib-linux-hci/clientlib/python/"
sys.path.append(FLIC_LIB_PATH)
import fliclib  # @UnresolvedImport
FLIC_HOST = "localhost"
LOGPATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
FILELOGLEVEL = logging.INFO
CONSOLELOGLEVEL = logging.WARN

flicClient = fliclib.FlicClient(FLIC_HOST)

eventhelper = EventHelper()

def initLogger(loggerName, logPath, fileLogLevel, consoleLogLevel):
    logger = logging.getLogger(loggerName)
    loggerLevel = min(fileLogLevel, consoleLogLevel)
    logger.setLevel(loggerLevel)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = handlers.TimedRotatingFileHandler(logPath, when='D', backupCount=7)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(fileLogLevel)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(consoleLogLevel)
    logger.addHandler(consoleHandler)
    
def handleButton(channel, click_type, was_queued, time_diff=None):
        try:
            logging.debug("handle Button called with " + str(click_type))
            if click_type == fliclib.ClickType.ButtonSingleClick:
                eventhelper.handleEvent(EventHelper.eventTypes["toggleFeed"])
            if click_type == fliclib.ClickType.ButtonDoubleClick:
                eventhelper.handleEvent(EventHelper.eventTypes["toggleWhite"])
            if click_type == fliclib.ClickType.ButtonHold:
                eventhelper.handleEvent(EventHelper.eventTypes["togglePrograms"])        
        except:
            logging.getLogger("flicintegration").error("handleButton failed" + traceback.format_exc())
                        
                        
def got_button(bd_addr):
    channel = fliclib.ButtonConnectionChannel(bd_addr)
    channel.on_button_single_or_double_click_or_hold = handleButton
    flicClient.add_connection_channel(channel)

def got_info(items):
    print(items)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        got_button(bd_addr)
        
initLogger("flicintegration", LOGPATH + "/piledcontrol_flicintegration.log", FILELOGLEVEL, CONSOLELOGLEVEL)
logging.getLogger("flicintegration").info("starting flicintegrator")


flicClient.get_info(got_info)

flicClient.on_new_verified_button = got_button

flicClient.handle_events()

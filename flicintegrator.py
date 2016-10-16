#!/usr/bin/env python3
# This caller relies on https://github.com/50ButtonsEach/fliclib-linux-hci
import sys
import traceback

from eventhelper import EventHelper 

FLIC_LIB_PATH = "/home/pi/fliclib-linux-hci/clientlib/python/"
sys.path.append(FLIC_LIB_PATH)
import fliclib
FLIC_HOST = "localhost"

flicClient = fliclib.FlicClient(FLIC_HOST)

eventhelper = EventHelper()
    
def handleButton(channel, click_type, was_queued, time_diff=None):
        try:
            print(str(click_type))
            if click_type == fliclib.ClickType.ButtonSingleClick:
                eventhelper.handleEvent(EventHelper.eventTypes["toggleFeed"])
            if click_type == fliclib.ClickType.ButtonDoubleClick:
                eventhelper.handleEvent(EventHelper.eventTypes["toggleWhite"])
            if click_type == fliclib.ClickType.ButtonHold:
                eventhelper.handleEvent(EventHelper.eventTypes["togglePrograms"])        
        except:
                print("toggleFeed failed" + traceback.format_exc())
                        
                        
def got_button(bd_addr):
    channel = fliclib.ButtonConnectionChannel(bd_addr)
    channel.on_button_single_or_double_click_or_hold = handleButton
    flicClient.add_connection_channel(channel)

def got_info(items):
    print(items)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        got_button(bd_addr)

flicClient.get_info(got_info)

flicClient.on_new_verified_button = got_button

flicClient.handle_events()

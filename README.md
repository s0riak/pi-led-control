# pi-led-control
## Introduction
pi-led-control enables you to control a single color RGB led strip attached to the GPIO pins of a raspberry pi running pi-blaster (https://github.com/sarfata/pi-blaster) with a webinterface.

pi-led-control is implemented as python webserver and a webui using jquery and bootstrap.
It provides several programs (scheduled and configurable) to control a single color LED strip.

##Requirements
###Hardware and pi-blaster
If you have a single color LED strip you need to connect it to your raspberry pi and setup pi-blaster.
You can find a very basic tutorial to connect a LED strip to your pi under https://github.com/s0riak/pi-led-control/blob/master/hardware/hardware.md
Please follow the instruction in https://github.com/sarfata/pi-blaster to setup pi-blaster.

###Mocking the LED strip
If you don't have a single color LED strip, you can use https://github.com/s0riak/pi-blaster-mock to mock it.

##Usage
To start pi-led-control execute:

main.py [-h] [-n NAME] [-p PORT] [-c CONFIGPATH] [-l LOGPATH]
    [-fl {0,10,20,30,40,50}] [-cl {0,10,20,30,40,50}]
    [-atc ACCESSLOGTOCONSOLE]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  the hostname on which pi-led-control is served
  -p PORT, --port PORT  the port on which pi-led-control is served
  -c CONFIGPATH, --configPath CONFIGPATH
                        the path to the config file to be used
  -l LOGPATH, --logPath LOGPATH
                        the path to the log folder to be used
  -fl {0,10,20,30,40,50}, --fileLogLevel {0,10,20,30,40,50}
                        the log level for the logfile
  -cl {0,10,20,30,40,50}, --consoleLogLevel {0,10,20,30,40,50}
                        the log level for the console
  -atc ACCESSLOGTOCONSOLE, --accessLogToConsole ACCESSLOGTOCONSOLE
                        set to True to print access log entries to console
   
   
The server is started locally and the UI can be accessed on http://localhost:9000 or the port specified.
### Logging
pi-led-control creates two log files:
piledcontrol.log - logging all relevant information on state changes and errors to a rotating logfile (1 per day, keeping those of last week) and stdout
piledcontrol_access - logging all requests and http error handled by pi-led-control to a rotating logfile (same rotation as for main log) and to stdout if ACCESSLOGTOCONSOLE is true

##Available programs

Several programs are available to control the LED strip:

0. 'Soft Off' to power off the LED strip smoothly (duration based on hue)
0. 'Off' to power off the LED strip immediately
0. 'Scheduled Off' to power off the LED strip after a given time in minutes (floats using '.' accepted for seconds are also accepted)
0. 'Full White' to power on all channel, resulting in maximum brightness
0. 'Feed' a configurable red light
0. 'Color Loop' a looping program rotating through the user defined colors
0. 'Wheel' a looping program smoothly switching from red to green to blue to red and so on
0. 'Sunrise' a program smooth illuminating the LED, simulating a sunrise
0. 'Freak' a program showing a new random color indefinitely at a userdefined pace
0. 'Random Path' a program smoothly switching between 'the' userdefined colors (from 'Color'-program) indefinitely at a userdefined pace
0. 'Color' a program with user selected color from a set of userdefined colors
0. 'Free Color' a program with a color the user can freely choose using three sliders for red, green, blue

The list of programs available in the ledui is about the same but naming is different but printed in the CLI program

##Status of the LED strip

The current color of the LED strip (as far as known to pi-led-control) is shown in the top right corner.

##Time initialization

To set the time of a sunrise(-program) the localtime system time is used.
Thus the timezone must be configured correctly, to wake at the expected time:
	
   sudo dpkg-reconfigure tzdata

##Automatic startup at boot
Add the following to your root crontab to autostart pi-blaster at start up of your system

   @reboot /home/pi/pi-blaster-master/pi-blaster

Add the following to your user crontab to autostart pi-led-control at start up of your system

   @reboot python3 /home/pi/pi-led-control/src/main.py

##Screenshots

![UI of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-main.png)
![Dialog for scheduled off program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-off.png)
![Dialog for sunrise program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-sunrise.png)
![Dialog for configuring the color program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-color.png)
![Dialog for editing a single color for the color program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-color-edit.png)
![Dialog for editing a single color for the color program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-loop-configure.png)
![Dialog for free color program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-freecolor.png)

##Environment
pi-led-control is currently only tested on Ubuntu 15.10 and Raspbian GNU/Linux 8 (jessie).

##Licences
pi-led-control is licensed under GPL and makes use of the following work:

0. bootstrap (https://github.com/twbs/bootstrap) licensed under the MIT License
0. jquery (https://github.com/jquery/jquery) licensed under the given license
0. IcoMoon-Free fonts (https://github.com/Keyamoon/IcoMoon-Free) licensed under the given CC BY 4.0 and GPL
0. bootstraptoggle (http://www.bootstraptoggle.com/) licensed under the MIT Licence
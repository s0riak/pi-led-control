# pi-led-control
## Introduction
This is a control server to set colors using a webinterface for pi-blaster (https://github.com/sarfata/pi-blaster).

pi-led-control is implemented as python webserver and a webui using jquery and bootstrap.
It provides several programs (scheduled and configurable) to control a single color LED strip.

##Usage
To start pi-led-control execute:

   python3 ledserver.py
   
The server is started locally and the UI can be accessed on http://localhost:9000.

Alternatively you can use an interactive CLI:

   python3 ledui.py

##Mocking the LED strip
If you don't have a single color LED strip, you can use https://github.com/s0riak/pi-blaster-mock to mock it.

##Available programs

Several programs are available to control the LED strip:

0. 'Soft Off' to power off the LED strip smoothly (duration based on hue)
0. 'Off' to power off the LED strip immediately
0. 'Scheduled Off' to power off the LED strip after a given time in minutes (floats using '.' accepted for seconds are also accepted)
0. 'Full White' to power on all channel, resulting in maximum brightness
0. 'Feed' a very dark red light
0. '4 Color Loop' a looping program showing blue, red, yellow, green
0. 'Wheel' a looping program smoothly switching from red to green to blue to red and so on
0. 'Sunrise' a program smooth illuminating the LED, simulating a sunrise
0. 'Freak' a program showing a new random color indefinitely
0. 'Random Path' a program smoothly switching between 'the' predefined colors indefinitely
0. 'Color' a program with user selected color from a set of predefined colors
0. 'Free Color' a program with a color the user can freely choose using three sliders for red, green, blue

The list of programs available in the ledui is about the same but naming is different but print in the CLI program

##Status of the LED strip

The current color of the LED strip (as far as known to pi-led-control) is shown in the top right corner.

##Time initialization

To set the time of a sunrise(-program) the localtime system time is used.
Thus the timezone must be configured correctly, to wake at the expected time:
	
   sudo dpkg-reconfigure tzdata

##Screenshots

![UI of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-main.png)
![Dialog for scheduled off program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-off.png)
![Dialog for sunrise program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-sunrise.png)
![Dialog for color program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-color.png)
![Dialog for free color program of pi-led-control](https://raw.githubusercontent.com/s0riak/pi-led-control/master/screenshots/pi-led-control-freecolor.png)

##Environment
pi-led-control is currently only tested on Ubuntu 15.10 and Raspbian GNU/Linux 8 (jessie).

##Licences
pi-led-control is licensed under GPL and makes use of the following work:

0. bootstrap (https://github.com/twbs/bootstrap) licensed under the MIT License
0. jquery (https://github.com/jquery/jquery) licensed under the given license
0. IcoMoon-Free fonts (https://github.com/Keyamoon/IcoMoon-Free) licensed under the given CC BY 4.0 and GPL
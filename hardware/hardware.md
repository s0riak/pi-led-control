# Hardware for pi-led-control
## Introduction
This tutorial describes how to connect a single color RGB LED strip with the GPIO pins of a raspberry pi so that it can be controlled by pi-blaster (https://github.com/sarfata/pi-blaster)

## Circuit Layout
Basically the component described here replaces the rgb-controller of any available single color RGB strip to make it controllable with the pi.
If you don't have a single color LED strip, you can use https://github.com/s0riak/pi-blaster-mock to mock it.

The component connects the power supply (of the original strip), led strip and the GPIO PINs of the raspberry pi using the following layout:
![circuit layout to control the led strip](https://raw.githubusercontent.com/s0riak/pi-led-control/master/hardware/circuit-layout.png)

## Board result 

**WARNING:**
Working with electronics is dangerous and might be restricted in your jurisdiction.
Please make sure that you know what you are doing!

Solder the components as shown in the circuit layout.

The result should look something like this:
![upside of the control board](https://raw.githubusercontent.com/s0riak/pi-led-control/master/hardware/upside.jpg)
Headers on the right hand side connects the GPIOs of the pi. Headers on the left drive the LED strip. Power supply is on the bottom right.
The Underside of the board: 
![underside of the control board](https://raw.githubusercontent.com/s0riak/pi-led-control/master/hardware/underside.jpg)
Headers on the right hand side connects the GPIOs of the pi. Headers on the left drive the LED strip. Power supply is on the top right.

## Shopping Cart

As it might be confusing for software guys ( ;) )to get the correct components here is a full list:
Component | Description | Quantity | approx. Price
--- | --- | --- | ---
TIP 120 STM | Transistor NPN-Darl TO-220 60V 5A 65W | 3 | 2,60€

SL 1X36G 2,54 | 36-pin header, straight, pitch 2.54 | 1 | 0,20€

BL 1X20G7 2,54 | 20-pin socket terminal strip, straight, RM 2.54, H: 7.0 mm | 1 | 1,00€

HEBW 25 | Barrel connector reverse print panel jack, solder tags | 1 | 0,30 €

HPR 50X100 | Matrix board, laminated paper, 50x100 mm | 1 | 0,40€

LITZE SW | Insulated braided copper wire, 10 m, 1 x 0.14 mm, black | 1 | 0,75€

LITZE BL | Insulated braided copper wire, 10 m, 1 x 0.14 mm, blue  | 1 | 0,75€

LITZE RT | Insulated braided copper wire, 10 m, 1 x 0.14 mm, red | 1 | 0,75€

LITZE BR | Insulated braided copper wire, 10 m, 1 x 0.14 mm, brown | 1 | 0,75€

LITZE GN | Insulated braided copper wire, 10 m, 1 x 0.14 mm, green | 1 | 0,75€

![Bits and pieces needed for the circuit](https://raw.githubusercontent.com/s0riak/pi-led-control/master/hardware/pieces.jpg)

The transistors used are Darlington transistors (https://en.wikipedia.org/wiki/Darlington_transistor)

## Acknowledgement
The following instructions helped in the creation of this guide:

0. http://www.forum-raspberrypi.de/Thread-hyperion-tutorial-ambilight-mit-standard-led-strips 
0. http://www.produktinfo.conrad.com/datenblaetter/150000-174999/150872-da-01-en-Transistor_TIP_120.pdf

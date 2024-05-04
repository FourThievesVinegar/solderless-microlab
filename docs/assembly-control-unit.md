# Microlab Control Unit Assembly

![Control Unit Exterior](/docs/media/microlab-control-unit.jpg)

## Electronic Parts:

Wires and Cables

- USB A/B cable for rPi to Arduino
- 1x female barrel plug connector (5.5mm x 2.1mm)
- 1x male barrel plug connector (5.5mm x 2.1mm)
- 1x KV-426 lever connector (i.e.: a 1-to-3 splitter for both + and - leads)
- 2x 2-wide lever nuts (or another way to join 4 small wires)
- 2x 3-wide lever nuts (or another way to join 6 small wires)
- 1x 12-pin panel-mounted female Phoenix-style connector
  - 3x the half of the stepper motor
- 1x 8-pin panel-mounted female Phoenix-style connector
- 1x 2-pin panel-mounted female Phoenix-style connector
  - 2x Quick disconnect connectors (if your 2-pin connector requires them)
- Cable materials (to connect to the Pumps Unit)
  - 2x 12-pin male Phoenix-style connector
  - 2x 8-pin male Phoenix-style connector
  - ~10 feet of 4-wire cabling cut into 2-foot lengths
- Assorted wire for inside the case (more 4-wire cable can be handy, especially the ribbon-style that can be easily split into individual wires)
- 5x male-to-female breadboard headers (at least). You want short headers so that they fit comfortably on the GPIO pins under the touchscreen.

Raspberry Pi

- Raspberry Pi 3 Model B Board (We have also successfully done preliminary testing on a Libre Computer Le Potato, although the touch-screen can be finicky)
- Raspberry Pi 3 b+ compatible display 3.5 inch TFT LCD Screen Kit, 3.5" 480x320 Resolution and XPT2046 touch controller
- Micro SD card, 32GB
  - Please note: we are aware that RPi hired a UK Spy Cop and were aggressively oblivious as to why that's a problem. For this and several other reasons, including increasing prices, we are investigating alternatives. We use "Raspberry Pi" as a short-hand for "single-board computer" (SBC) and encourage experimentation with Libre Computer and other replacements.
- Arduino
- Arduino UNO SMD Rev3
- CNC Shield - Expansion Board V3.0 +UNO R3 Board 
- 4x A4988 Stepper Motor Driver with Heatsink (K75-CNC-UK)
- Stepper motor drivers (quantity 4)
- Misc
- 3x Individual relays that can switch 12v and be activated by as low as 3.3v. Typically these are small and blue and come on their own little circuit board. A single 4-relay board will also work.
- 1x Buck Converter module (to step down 12v to 5v). Must have at least two 5v outputs.
- 1x Button-style switch for the reactor light.
- Double-sided velcro straps for wire management and for holding components in place (optional, but highly recommended)

## Printed Parts

- Control Unit box
- Control Unit lid

## Raspberry Pi Formatting/Setup

### Putting OS and Microlab software on an SD card

1. Install Raspberry Pi Imager onto a computer.
1. Download our disk image torrent from [our website](https://fourthievesvinegar.org/microlab/).
   1. Please continue to seed the torrent!
   1. This image is a version of the OS with the Microlab software already installed.
      1. The production image already has drivers for the LCD screen installed - you MUST use the touchscreen with the production image.
      1. The development image uses the HDMI port and requires an external monitor.
      1. If you plan to do extensive development on an external monitor, you can cut or drill a hole in the side of the case to allow an HDMI cable to pass through.
      1. The external USB ports can be used to attach a mouse and keyboard for development or ease of use.
      1. NOTE: The touch screen is primarily used for mobility and portability. Users familiar with networking may also choose to run the lab “headless”, and connect across a network without a monitor or USB input devices.
      1. NOTE: The production image has drivers for the 3.5" display using goodtft and XPT2046 touch controller drivers. If you have a different display, you will need to use the development image, then download and install the appropriate drivers. The development image requires using an external monitor.
1. Connect the MicroSD card to your computer. You may need an SD card to USB converter. [part #]
1. Launch the Raspberry Pi Imager.
1. Select “Choose OS”, and scroll down to “Use Custom”.
1. Select the downloaded [imagefile].
1. Click “storage”, and select your SD card.
1. Click “Write”.
1. Allow the Raspberry Pi Imager program to write to the SD card.
1. The imager program will also run a verification check to make sure the OS was installed correctly. This will take several minutes.

### Installing SD the card

1. Once complete, remove the SD card from your computer, and insert into your Raspberry Pi.
1. Note that the SD card extends beyond the edge of the Pi's circuit board. The Pi is very delicate with the card inserted, so take care.

### Installing the touchscreen

1. Gently slide the screen's female headers over the Pi's GPIO pins.
1. The screen should line up with the Pi's board and the end of the headers should aldo coincide.

## Arduino Setup
1. Before assembling, follow the instructions [here](https://github.com/gnea/grbl/wiki/Compiling-Grbl) to compile and flash grbl to the arduino
   1. Detailed pin diagram here [https://blog.protoneer.co.nz/arduino-cnc-shield-v3-00-assembly-guide/](https://blog.protoneer.co.nz/arduino-cnc-shield-v3-00-assembly-guide/)
   1. Note: Video overview of CNC shield assembly and operation [https://youtu.be/zUb8tiFCwmk?t=37](https://youtu.be/zUb8tiFCwmk?t=37)
   1. Note: Critical safety information when working with the CNC shields. Failure to follow them can hurt both you and the component. NEVER connect or disconnect any stepper motor to the CNC Shield while the power is on or connected
   1. ALWAYS disconnect the power before connecting or disconnecting the stepper motors
   1. When installing the motor driver, be sure to correctly orient the driver so the enable pin matches the EN pin on the CNC Shield. **The A4988 driver has a small potentiometer on the BOTTOM center of the circuit board**, and the EN pin is on the top left. Make sure you have installed the drivers correctly per the manufacturer's instructions.
   1. ALWAYS connect a stepper motor to the CNC Shield when testing or using it. If a stepper motor is not connected it can cause the driver to overheat and become damaged.
   1. When attaching the heatsink to the drivers, it is critical that the heatsink is centered on the chip and does not contact any of the pins. Failure to correctly place the heatsink can cause the driver to short out and fail.
   1. (video part 1: 00:18 WARNING: video incorrectly shows installing all 4 drivers) Mount the motor control drivers (MC-MDR) on the CNC hat (MC-CNC). The four drivers are labeled X, Y, Z, and A. Since this project only requires three stepper motors, we will only use sockets X, Y, and Z. To ensure you have the orientation correct, orient the CNC hat so that the 12v power connection is in the lower left, the reset button is in the upper left. Orient each of the A4988 drivers so that the small potentiometer (looks like a small phillips head screw) is toward the bottom of the board.
      1. Double check that you have installed the drivers according to the manufacturer's instructions.
      1. Double check that all of the drivers are firmly seated in the sockets, and that none of the heat sinks shifted during installation.
   1. Mount the CNC Hat on the Arduino. The 12v power connection on the lower left of the hat should be directly above the Arduino power jack also on the lower left.

### Verify stepper motor wires and tune the potentiometers

You can do this step before assembling the Reactor if you have:

- A working Pi,
- a working Arduino with the motor shield connected to a 12v power source,
- stepper motors or stepper-driven peristaltic pumps, and
- the stepper motor cables.

You can also perform this step after assembling the other units, but you DEFINITELY want to tune the potentiometers. If you don't, the stepper motors will likely behave very strangely and could be damaged by excess voltage. You can use the Test Recipe on the Microlab to do this, which has an option to manually run each of the reagent pumps, as well as activing the stirrer and heating tools. You can also do this after assembling the other units, but be sure to do it before you close the lid on the Control Unit.

#### Motor board potentiometer tuning

TODO: GET IMAGE OF POTENTIOMETER

**WARNING!** Failure to correctly tune the potentometers can damage the motor controller and the motors themselves.

To tune them, **gently** turn the potentometers on the motor control boards clockwise using a small phillips head screw driver, taking care not to turn past any resistance. Turning them clockwise "closes" the voltage down while turning them counter-clockwise "opens" the voltage up. Start with the potentiometers in the "closed" position, and slowly "open" each of them a quarter of a turn at a time until the stepper motors respond correctly - they should turn smoothly. If they do not move, "open" the potentometer an eighth-turn and try again. If they move erratically, your voltage is likely too high.

![Assembled controller boards](/docs/media/rasp_pi2.png)
![Assembled controller boards](/docs/media/arduino.png)

#### Stepper motor verification

If you have trouble with the pumps, you may want to verify that your stepper motors are wired correctly and that your control board is calibrated. Each motor will have four different color wires. To verify that the motor is wired in a way that is compatible with the CNC Hat, you need to identify the pairs of wires that feed the two coils inside the motor. **It is likely that the cables that came with the stepper motors will *just work* but verification can be helpful if you run into trouble.** 

With the motor disconnected, you should be able to spin the shaft with your fingers and feel almost no resistance. Take a short length of wire and jumper the top two pins (Pins 1 and 2) of the connector together. If the motor is wired correctly you should now feel some resistance when you spin the shaft (you should be able to feel the “steps” in the stepper motor). Repeat this procedure with the bottom two pins (Pins 3 and 4). If you do not feel any change in resistance, try jumpering other combinations of pins until you identify the two pairs. It is ESSENTIAL that the top two pins form a pair, and the bottom two pins form a pair, but the order of the wires within each pair does not matter. For example, if you find that pins 1 and 3 are a pair, you will need to rewire the connector so that these two are the top pair, and pins 2 and 4 are the bottom pair.

## Control Unit assembly

With the release of v0.6 of the microlab, all cases and housings are now 3D printed. The Control Unit box and lid are designed to support all components and ports that comprise the unit. Because the control unit has by far the most sub-components of any of the Microlab modules, we have broken down the instructrions by sub-assembly.

### Mounting the components to the case

**Components:**

TODO: List of components

### Installing the external plugs

- Power inlet
- Phoenix connectors
  - 12-pin, 8-pin (only the parts that mount to the case.)
  - and 2-pin
- Button
- USB ports

### Assembling the 8-pin relay sub-assembly

### Assembling the 12-pin stepper sub-assembly

### Attaching straps (optional)

### Mounting the 8-pin and 12-pin sub-assemblies

- Connect the button

### Wiring the 12V and USB power

### Connecting the GPIO Pins

### Final mounting and assembly

Before you finish close the case, you probably want to test that everything is wired correctly. We **highly** recommend testing all the functionality of the Microlab using the Test Recipe. Of course, if something doesn't work right or stops working in the future, you can always open it back up again.

### Ribbon Cables


Once everything is connected, the inside of your box should look something like this:

TODO: GOOD INTERIOR PIC OF CONTROL UNIT

NOTE: In this image, the relay board is separated from the Pi (rather than using a relay hat). 

It is possible to wire everything together using less-expensive soldering techniques or wire nuts, but the lever connectors are very easy to assemble and reconfigure as needed.
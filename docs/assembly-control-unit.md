# Microlab Control Unit Assembly

![Control Unit Exterior](/docs/media/microlab-control-unit.jpg)

**Some notes:**

- The Microlab is designed to be assembled without the need for soldering or other specialized tooling. If you are equipped to solder, you can construct one at a lower cost and with less junk in the case by replacing the lever-action wire connectors with solder joints (or screw cap connectors).
- Additionally, you can save space in the case by splicing wires and modifying components like USB cables to remove extraneous material.

TODO: Pic comparing stock and modified micro USB

## Electronic Parts

### Wires and Cables and Connectors (Oh my!)

- USB A/B cable for rPi to Arduino
- USB A cable (cut off with + and - wires exposed and stripped)
- Micro USB cable to power the rPi (check your SBC to see which cable is appropriate)
- Female barrel plug connector (5.5mm x 2.1mm)
- Male barrel plug connector (5.5mm x 2.1mm)
- KV-426 lever connector (i.e.: a 1-to-3 splitter for both + and - leads)
- 2x 2-wide lever nuts (or another way to join 4 small wires)
- 2x 3-wide lever nuts (or another way to join 6 small wires)
- 12-pin panel-mounted female Phoenix-style connector
  - 3x the half of the stepper motor cables that connect to the motor control board
- 8-pin panel-mounted female Phoenix-style connector
- 2-pin panel-mounted female Phoenix-style connector
  - 2x Quick disconnect connectors (if your 2-pin connector requires them)
- Cable materials (to connect to the Pumps Unit)
  - 2x 12-pin male Phoenix-style connector
  - 2x 8-pin male Phoenix-style connector
  - ~10 feet of 4-wire cabling cut into 2-foot lengths
- Assorted wire for inside the case (more 4-wire cable can be handy, especially the ribbon-style that can be easily split into individual wires)
- 5x male-to-female breadboard headers (at least). You want short headers so that they fit comfortably on the GPIO pins under the touchscreen.

### Raspberry Pi

- Raspberry Pi 3 Model B Board (We have also successfully done preliminary testing on a Libre Computer Le Potato, although the touch-screen can be finicky)
- Raspberry Pi 3 b+ compatible display 3.5 inch TFT LCD Screen Kit, 3.5" 480x320 Resolution and XPT2046 touch controller
- Micro SD card, 32GB
  - Please note: we are aware that RPi hired a UK Spy Cop and were aggressively oblivious as to why that's a problem. For this and several other reasons, including increasing prices, we are investigating alternatives. We use "Raspberry Pi" as a short-hand for "single-board computer" (SBC) and encourage experimentation with Libre Computer and other replacements.
- Arduino
- Arduino UNO SMD Rev3
- CNC Shield - Expansion Board V3.0 +UNO R3 Board 
- 4x A4988 Stepper Motor Driver with Heatsink (K75-CNC-UK)
- Stepper motor drivers (quantity 4)

### Misc

- 3x Individual relays that can switch 12v and be activated by as low as 3.3v. Typically these are small and blue and come on their own little circuit board. A single 4-relay board will also work.
- Buck Converter module (to step down 12v to 5v). Must have at least two 5v outputs.
- Button-style switch for the reactor light.
- Double-sided velcro straps for wire management and for holding components in place (optional, but highly recommended)
- Assorted M3 screws (TODO: Which lengths and how many?)

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

You can also perform this step after assembling the other units. You **DEFINITELY** want to tune the potentiometers. If you don't, the stepper motors will likely behave very strangely and could be damaged by excess voltage. You can use the Test Recipe on the Microlab to do this, which has an option to manually run each of the reagent pumps, as well as activing the stirrer and heating tools. You can also do this after assembling the other units, but be sure to do it before you close the lid on the Control Unit.

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

### Attaching straps (optional)

The Control Unit box has holes in the bottom to accomodate short M3 screws to hold velcro straps in place. These straps can hold the Buck Converter and relays in place. They are optional, but highly recommended if you will be shipping your Microlab or otherwise expect it to get jostled. Be sure to cut the straps long enough to wrap around your components. Experiment with placing the Buck Converter and relays on the left side of the case to make sure they will fit under the Pi.

### Assembling the 8-pin relay sub-assembly

This is where much of the wiring inside the Control Unit happens. If you get through this step, you'll be well on your way to assembling the Control Unit.

TODO: Pic of components
TODO: Pic of assembled assembly

**Components:**

- 8-pin female Phoenix connector (the part with screw terminals that the other part with the screw terminals fit into)
- 3x individual relays (or 4x relay board)
- 2x 2-wide lever nuts (or another way to join 4 small wires)
- 2x 3-wide lever nuts (or another way to join 6 small wires)
- Assorted wires
  - 3x red wires and 3x black wires (for 5v relay power - only one of each is needed for a 4x relay board)
  - 3x short wires (for connecting the relays to the 8-pin Phoenix connector - preferably color-coded)
  - 2x 4-wire cables (for connecting the relays to the +12v power and the 8-pin Phoenix connector to the -12v power)
- 3x male-to-female leads (for signaling from Pi to relays)
- USB cable (cut off with the "A" side intact and the + / - wires exposed and stripped)

**Assembly:**

TODO: Detail assembly

### Assembling the 12-pin stepper sub-assembly

TODO: Pic of assembly

**Components:**

- 1x 12-pin panel-mounted female Phoenix-style connector
- 3x the half of the stepper motor cables that connect to the motor control board

**Assembly:**

- Use a small screwdriver to open the screw terminals on the 12-pin Phoenix receptacle.
- Cut, strip, and insert the wires into the 12 screw terminals, tightening them down one-by-one
- NOTE: There are 8 total places where we will be screwing wires into Phoenix connector screw terminals, each of which is an opportunity to make a mistake by changing the order of the wires. The key is to ensure that the wiring is consistent across all connections (i.e.: the leftmost wire stays the leftmost in all the junctions and cables and all other wires are also in the same order.)

### Mounting the components to the case

Mount the panel-mounted components to the case. 

TODO: Pic of components
TODO: Pic of case with components mounted

**Components:**

- 1x female barrel plug connector (5.5mm x 2.1mm)
- Phoenix connectors
  - 12-pin assembly and 8-pin assembly
  - and 2-pin connector
- Button
- USB ports

**Assembly:**

- Feed the 12-in and 8-pin sockets through the appropriate holes on the front of the case, then clip them into the Phoenix connector mounting pieces.
- Use M3 screws to mount the Phoenix connectors to the case in the matching two holes in the front and the smaller rectangular hole in the back.
  - For now, pull as much of the assemblies as possible out of the box so that you can easily position the other components.
- Insert the button in the circular hole on the left side and attach with the matching nut.
- Insert the female barrel plug connector in the circular hole on the back side and attach with the matching nut.
- USB ports mount to the front of the case and should come with their own screws.
- If the circular holes are too small or the pre-printed holes don't fit your USB ports, you can use a drill to widen or add new holes.

### Wiring the 12V and USB power

This is where we connect most of the rest of the parts.

**Components:**

- 1x Male barrel plug connector (5.5mm x 2.1mm)
- 1x KV-426 lever connector (i.e.: a 1-to-3 splitter for both + and - leads)
- 1x Buck Converter module

**Assembly:**

- Insert the wires for the female barrel plug connector into the 1x side of the lever connector.
- Insert the wires for the male barrel plug connector into the 3x side of the lever connector.
  - Note: You should be able to insert up to 2 wires into each socket on the lever connector. Twisting wires together may make this easier.
  - Note: **Make sure the wires are sufficiently stripped!** If the lever connector closes on the wire's insulation, it will not work!
- Plug the male barrel plug connector into the Buck Converter module.
- Plug the USB cable for the Pi and the USB cable for the relays into the USB ports on the Buck Converter.
- Position the Buck Converter as far to the left side of the case as possible. If using straps, find an appropriate position to attach the strap the case by punching a hole in a piece of two-sided velcro and inserting a short M3 screw, then screwing it into a hole on the case bottom.
- Insert the + and - wires from the 8-pin relay sub-assembly into the 3x side of the lever connector
- Following the manufacturer's instructions, insert the + and - leads for the button light into the 3x side of the lever connector - this way the button light will turn on whenever the Control Unit is powered.

### Connecting the GPIO Pins

The GPIO pins are how the Pi switches the relays.

TODO: Pic of connected GPIO pins

**Components:**

- 5x male-to-female breadboard headers
  - 3 of these will be from the 8-pin relay sub-assembly
- 2x quick-disconnect connectors (or other appropriate connector for your 2-pin Phoenix connector)

**Assembly:**

- Use pliers or wire strippers to crimp the quick disconnect connectors onto the new male headers. Gently tug to make sure they are secure. If they come out, re-insert and continue crimping.
- Connect the quick disconnect connectors to the 2-pin Phoenix port, making sure that the contacts are securely in place.
- Mate the female headers with the GPIO pins on the Pi. Check the `ftv_microlabv0.5.0.yaml` file for mappings. They should be:
  - Stirrer: 16
  - Heater: 26
  - Heater pump: 20
  - Cooler pump: 21

### Final mounting and assembly

Before you close the case, you probably want to test that everything is wired correctly. We **highly** recommend testing all the functionality of the Microlab using the Test Recipe. Of course, if something doesn't work right or stops working in the future, you can always open it back up again.

NOTE: As you put things into the case, you may notice that the long wires that made things easy to work with during assembly are now getting in the way of things. Feel free to cut internal wires shorter - with non-solder connectors, this shouldn't be too hard.

### Ribbon Cables

To connect the Control Unit to the Pumps Unit, we will use a pair of ribbon cables: 8-wire and 12-wire. Savvy readers will notice that this corresponds with the Phoenix connectors.

When this step is complete, you will have two cables that plug into the ports on the Control Unit and the Pumps Unit. It should not matter which end of the cable is in which unit. Make sure that the wire order is consistent at both ends of the cables.

**Components:**

- ~10 feet of 4-wire cabling cut into 5 2-foot lengths
- 2x 8-pin male Phoenix connectors
- 2x 12-pin male Phoenix connectors

**Assembly:**

- Cut and strip the cables so that the wire ends can be inserted into the phoenix connectors.
- Insert the wires into the Phoenix connectors and tighten the screw terminals closed, one-by-one.
- NOTE: This is another place where wires can get crossed. To ensure proper connectivity between the Control Unit and the Pumps Unit, make sure that the wires are consistently placed. One way to do this is to plug the Phoenix connectors together and make sure that each wire retains its position from left to right when viewed from the front. You will also need to make sure that the wiring in the Pump Unit is consistent with this.

## Testing the unit

Once everything is connected, the inside of your box should look something like this:

TODO: GOOD INTERIOR PIC OF CONTROL UNIT

NOTE: In this image, the relay board is separated from the Pi (rather than using a relay hat). 

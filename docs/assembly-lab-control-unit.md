# Microlab Lab Control Unit Assembly

![Control Unit Exterior](/docs/media/microlab-control-unit.jpg)

## Electronic Parts:

- USB A/B cable for rPi to Arduino
- Power cables
- Micro SD card, 32GB
- Raspberry Pi
  - Raspberry Pi 3 Model B Board
  - Raspberry Pi Expansion Board 4 Channel Relay Board
  - Raspberry Pi 3 b+ Display 3.5 inch TFT LCD Screen Kit, 3.5" 480x320 Resolution
- Arduino
  - Arduino UNO SMD Rev3
  - CNC Shield - Expansion Board V3.0 +UNO R3 Board + A4988 Stepper Motor Driver with Heatsink (K75-CNC-UK)
  - CNC shield - A4988 V3 Engraver Drive Shield 3D Printer CNC Drive Expansion Board for Ardulno 3D Printer CNC (2 pcs)
  - Stepper motor drivers (quantity 4)

1. Raspberry Pi Formatting/Setup

   1. Putting OS and Microlab software on SD card\*\*
   1. Install Raspberry Pi Imager onto a computer.
   1. Download our disk image torrend from [our website](https://fourthievesvinegar.org/microlab/).
        1. Please continue to seed the torrent!
       1. This image is a version of the OS with the Microlab software already installed.
   1. Connect the MicroSD card to your computer. You may need an SD card to USB converter. [part #]
   1. Launch the Raspberry Pi Imager.
   1. Select “Choose OS”, and scroll down to “Use Custom”.
   1. Select the downloaded [imagefile].
   1. Click “storage”, and select your SD card.
      Click “Write”.
   1. Allow the Raspberry Pi Imager program to write to the SD card.
   1. The imager program will also run a verification check to make sure the OS was installed correctly. This will take several minutes.

   1. Installing SD card
      1. Once complete, remove the SD card from your computer, and insert into your Raspberry Pi.
      1. Power on the Pi, and allow it to boot.
          1. The production image will already have drivers for the LCD screen installed. The development image will not.
      1. NOTE: The touch screen is primarily used for mobility and portability. The program can also be run on a regular monitor connected via HDMI, as well as a USB Keyboard and mouse. Users familiar with networking may also choose to run the lab “headless”, and connect across a network without a monitor or USB input devices.
   1. Installing [Microlab Software] without image use.
      1. This is for advanced users who wish to install the software manually, rather than starting from a clean OS install.
      1. Ubuntu is the recommended OS for this use
      1. See Appendix B. Headless Install

1. Arduino Setup
   1. Before assembling follow the instructions [here](https://github.com/gnea/grbl/wiki/Compiling-Grbl) to compile and flash grbl to the arduino
   1. Detailed pin diagram here [https://blog.protoneer.co.nz/arduino-cnc-shield-v3-00-assembly-guide/](https://blog.protoneer.co.nz/arduino-cnc-shield-v3-00-assembly-guide/)
   1. Note: Video overview of CNC shield assembly and operation [https://youtu.be/zUb8tiFCwmk?t=37](https://youtu.be/zUb8tiFCwmk?t=37)
   1. Note: Critical safety information when working with the CNC shields. Failure to follow them can hurt both you and the component. NEVER connect or disconnect any stepper motor to the CNC Shield while the power is on or connected
   1. ALWAYS disconnect the power before connecting or disconnecting the stepper motors
   1. When installing the motor driver, be sure to correctly orient the driver so the enable pin matches the EN pin on the CNC Shield. The A4988 driver has a small potentiometer on the bottom center of the IC board, and the EN pin is on the top left. Make sure you have installed the drivers correctly per the manufacturer's instructions.
   1. ALWAYS connect a stepper motor to the CNC Shield when testing or using it. If a stepper motor is not connected it can cause the driver to overheat and become damaged.
   1. When attaching the heatsink to the drivers, it is critical that the heatsink is centered on the chip and does not contact any of the pins. Failure to correctly place the heatsink can cause the driver to short out and fail.
   1. Mount the heat sinks on the motor control drivers (MC-MDR) with thermal adhesive, making sure that the heat sink does not contact any of the pins.
   1. (video part 1: 00:18 WARNING: video incorrectly shows installing all 4 drivers) Mount the motor control drivers (MC-MDR) on the CNC hat (MC-CNC). The four drivers are labeled X, Y, Z, and A. Since this project only requires three stepper motors, we will only use sockets X, Y, and Z. To ensure you have the orientation correct, orient the CNC hat so that the 12v power connection is in the lower left, the reset button is in the upper left. Orient each of the A4988 drivers so that the small potentiometer (looks like a small phillips head screw) is toward the bottom of the board.
   1. Double check that all of the drivers are firmly seated in the sockets, and that none of the heat sinks shifted during installation.
   1. Mount the CNC Hat on the Arduino. The 12v power connection on the lower left of the hat should be directly above the Arduino power jack also on the lower left.

![Assembled controller boards](/docs/media/rasp_pi2.png)
![Assembled controller boards](/docs/media/arduino.png)

## Lab Control Unit Housing assembly

With the release of version 0.5 of the Microlab, we recommend enclosing the Lab Control Units in an enclosure that provides protection to the components and standard interfaces to the other units. This enclosure can be produced using corrugated plastic or another rigid, durable, waterproof material that you are comfortable cutting and shaping into a box. Because folded corrugated plastic tends to return to its original position, it may be necessary to cut off tabs and re-attach them with duct tape, which provides more flexibility. The pictured enclosure is 8" x 6" x 4" and fits all of the Lab Control Unit components comfortably inside. We also recommend a small 5v fan to ensure air flow. Components and velcro straps can be attached to the enclosure using short M3 screws, washers, and nuts.

### Cutting the housing

- Cut a hole for the display (take care measuring so that the hole fits the screen as closely as possible). 
- Cut holes for the cables, the barrel plug connectors (if using them), and the button for the light (if using it)
- We also recommend cutting holes for a fan to prevent overheating

The Lab Control Unit enclosure is designed to be as modular as possible. In this image, the cables for the Reagent Pump Unit and thermistor are fixed, but cables for the circulation pumps, reaction chamber light, mixing motor, and Temperature Control Unit provide standard interfaces for cables. The knob is an optional PWM motor speed controller that allows manual control over the mixing motor's speed.

**Note: The image below shows two plugs for the circulation pumps. The latest design uses only one pump.

![Control Unit Interfaces](/docs/media/microlab-control-unit-interface.jpg)

### Mounting the components

#### Securing them to the case
- Inside the enclosure, connect the extension cord, 5v, and 12v power supplies ("wall warts") to the enclosure with velcro straps. 
- Attach the straps to the case using small M3 screws. 
   - You can use similar screws to connect the larger lever connectors, the arduino, and the relay break-out board (if you are using it instead of the Pi hat). 
   - You can use similar straps to hold the display and the Pi in place.
   - Basically, everything is going to be strapped in and the straps are bolted down
   - You can also attach small velcro straps to bundle wires and reduce the "rats nest" factor

#### Installing the external plugs
The interface to the other components are standard female barrel plug connectors.
- Insert the leads for these through the holes you cut previously 
   - Cut away any excess housing material on the threads
   - Secure to the enclosure with the connectors' threaded nuts

### Wiring the components together

There are several connections to make inside the housing. Make sure the main power extension cord is unplugged when making these connections!

#### Wiring the 12v manifold
- Connect the 12v "wall wart" into the input of the lever connector splitter.
    - We recommend using a barrel plug connector between components to avoid directly modifying (cutting and splicing) off-the-shelf components. This improves modularity and allows you to swap out parts more easily later.
- Use lever connectors as needed to connect the leads from the external barrel plug connectors to the 12v power, as well as to the appropriate relays. Make sure to strip the wires sufficiently as the lever connectors will not work if they clamp onto the insulated section of the wire.
   - The relays inside the Lab Control Unit switch the stirring motor and circulation pump. There is also a relay in the Temperature Control Unit power block - this is switched directly by a GPIO pin and will be discussed later.
   - If you're not sure which relays are which, consult the documentation for your relay hat or board.
   - Consult the pin diagram for your Pi for which GPIO pins to connect to the relay board if you are using a separate relay breakout board like the one pictured here.
   - See `backend/hardware/base_hardware.yaml` for which GPIO pins activate which systems
- If you have a reactor light and a button to use it with, wire the button according to its instructions and connect it to the appropriate barrel plug connector.
- Connect the 12v barrel plug input on the Arduino's motor control board to the 12v power supply

#### Wiring the 5v components
- Connect the 5v "wall wart" to the Pi.
    - For simplicity, we connected things as follows: 5v power > Raspberry Pi > USB cable > Arduino Motor Control Shield Stack > 5v Manifold > Relay board + Fan + Temperature Control Unit power block relay.
    - You may want to connect the "wall wart" directly to the 5v manifold and connect the Pi and the other 5v components separately.
- Set up a +/- 1-to-3 lever connector to use as a splitter and connect the components to it.
    - As input, you can use the +5v or +3v and GND from the motor control shield.
    - The relay board and fan both require 5v power. 
    - So does the Temperature Control Unit's Power block. Connect two of the wires from the 3 wire connector to the manifold. The remaining wire will be connected to a GPIO pin.

#### USB connections
- Connect the temperature probe and motor control shield to the USB ports on the Pi. 
- You may also want to add a short male-to-female USB cable to more easily connect to peripherals like a keyboard.

#### GPIO Pins
- If using a separate relay board:
    - Connect wires to the GPIO pins on the Pi's board.
    - See `backend/hardware/base_hardware.yaml` for which GPIO pins activate which systems.
    - Connect the pins that control the stirrer motors and heating circulation to the appropriate inputs on the relay board.
    - Connect the pin that controls the Temperature Control Unit's relay to the third wire on the 3 wire connector.
- If using a "Pi Hat" relay board, you will only need to run a wire to the pin that switches the Temperature Control Unit's relay, connecting it to the third wire in the 3 wire connector.

#### Stepper motor cables

- Bundle the stepper motor cables together
   - Wrap the 3 stepper motor control cables in the split loom cable wrap (optional, but highly recommended!)
      - We also recommend you label both ends of the cables with tape!
   - Feed the 4-wide end of the cables (not the 6-wide - those plug into the motors!) and the cable wrap into the housing through the hole you made
   - Secure the cables inside the cable wrap (tight zip ties are good for this) and secure the cable wrap to the enclosure using copius amounts of electrical tape. The goal is to prevent cables from being yanked loose or damaging components when tugged from the outside
- Connect the stepper motor control cables to the motor control board
   - Connect each of the X, Y, and Z cables to the appropriate spot on the motor control board

Once everything is connected, the inside of your box should look something like this:

![Control Unit Interior](/docs/media/microlab-control-unit-inside-labeled.jpg)

NOTE: In this image, the relay board is separated from the Pi (rather than using a relay hat). 

It is possible to wire everything together using less-expensive soldering techniques or wire nuts, but the lever connectors are very easy to assemble and reconfigure as needed.
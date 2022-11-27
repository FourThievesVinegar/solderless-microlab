# Microlab Assembly

&nbsp;

## Building a Microlab (Instructions currently incomplete)

![Built Microlab](/docs/media/microlab.png){: style="height:90%;width:90%"}

The Microlab consists of three major parts:

1. Reaction chamber
1. Syringe pumps
1. Control boards

**Reaction Chamber**
The central part of the Microlab is the reaction chamber. It consists of a custom 3D printed Mason jar lid (called the reactor manifold) that allows a small mason jar to nest into a larger, wide-mouthed mason jar. During operation, the large mason jar will be filled with water. Holes in the mason jar lid will allow a pair of pumps to pump in hot or cold water to control the temperature of the water inside the large, outer mason jar. A stir rod with paddle will mix the chemicals in the smaller jar.

**Syringe Pumps**
The Microlab uses two 3D printed syringe pumps to insert additional chemicals into the inner mason jar reactor when certain conditions are met. These syringe pumps have syringes inserted into them, and are attached to stepper motors that are controlled by the control boards to automate the syringe pumps.

**Control Boards**
The control boards are the brains of the device. Consisting of an Arduino microcontroller (a programmable circuit board) and a Raspberry Pi (a mini computer).

The Arduino controls the syringe pumps, while the Raspberry Pi follows the recipe that it has been ordered to execute, controls the stirrer and temperature control pumps, monitors the temperature of the Lab Reactor, and the reaction time.

### Safety

See Appendix.

### Materials

![Parts laid out on table](/docs/media/parts_label.png){: style="height:90%;width:90%"}

Fig. 1 Parts Photo
&nbsp;

### Parts List

&nbsp;
The boards, components and parts needed for this project are located in the Bill of Materials (BOM) file.

Download the BOM here: [https://github.com/FourThievesVinegar/solderless-microlab/tree/master/docs/Microlab Parts List.xlsx](https://github.com/FourThievesVinegar/solderless-microlab/tree/master/docs/Microlab%20Parts%20List.xlsx)

### 3D Printed Parts

While most items on the parts list can be purchased, a few items will need to be printed using a 3D printer:

- syringe pumps
- reactor manifold
- motor mount
- heating vessel lid
- cooling vessel lid
- tube fittings (can be purchased, but they are in the parts repo)
- raspberry pi case (not yet uploaded)

Parts files are available here: [https://github.com/FourThievesVinegar/Parts/](https://github.com/FourThievesVinegar/Parts/)

**Syringe pumps**

**Quantity: 2**

The syringe pump is made up of 8 parts that must be printed. The parts are labelled Linear Actuator with a part number.
https://www.youmagine.com/designs/syringe-pump
![Syringe pump](/docs/media/syringe_pump2.png){: style="height:30%;width:30%"}

**Reactor manifold**

**Quantity: 1**

This 3D printed lid allows the smaller jar to nest inside the larger jar of the reaction chamber, [STL available here](https://github.com/FourThievesVinegar/Parts/blob/master/v4/reactorManifold_v0.7.STL).


**Inspect 3D printed part**
Before assembly, be sure to inspect the parts that have come out of the 3D printer.

1. Ensure the inner reactor (part [x]) and outer reactor (part [y]) can be screwed into the Reactor Manifold (Part 3D [xx]).
1. Check to make sure all screw holes are open. Use a drill to clear them if needed
1. Check to make sure the holes on the [center part] are open to allow guide rods and the threaded rod to pass thru. Use a drill to clear them of excess print material if needed.

## Instructions

### Controller Boards Assembly

![Assembled controller boards](/docs/media/controller_boards.png){: style="height:30%;width:30%"}

#### Parts:

- 3D printed case
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
   1. Download [The Imaged version of the OS from Github] from [file location].
   1. This image is a version of the OS with the Microlab software already installed. ( See [7.2] for steps to install the microlab software without using the pre-packaged image file.)
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
      1. Install drivers (optional)
      1. Install the drivers for the touchscreen, if using.
      1. Follow instructions from the touchscreen manufacturer.
      1. NOTE: The touch screen is primarily used for mobility and portability. The program can also be run on a regular monitor connected via HDMI, as well as a USB Keyboard and mouse. Users familiar with networking may also choose to run the lab “headless”, and connect across a wireless network without a monitor or USB input devices.
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
   1. When installing the motor driver, be sure to correctly orient the driver so the enable pin matches the EN pin on the CNC Shield. The A4988 driver has a small potentiometer on the bottom center of the IC board, and the EN pin is on the top left.
   1. ALWAYS connect a stepper motor to the CNC Shield when testing or using it. If a stepper motor is not connected it can cause the driver to overheat and become damaged.
   1. When attaching the heatsink to the drivers, it is critical that the heatsink is centered on the chip and does not contact any of the pins. Failure to correctly place the heatsink can cause the driver to short out and fail.
   1. (Not shown in video) Mount the heat sinks on the motor control drivers (MC-MDR) with thermal adhesive, making sure that the heat sink does not contact any of the pins.
   1. (video part 1: 00:18 WARNING: video incorrectly shows installing all 4 drivers) Mount the motor control drivers (MC-MDR) on the CNC hat (MC-CNC). The four drivers are labeled X, Y, Z, and A. Since this project only requires two stepper motors, we will only use sockets Y and A on the right side of the board. To ensure you have the orientation correct, orient the CNC hat so that the 12v power connection is in the lower left, the reset button is in the upper left. Orient each of the A4988 drivers so that the small potentiometer (looks like a small phillips head screw) is toward the bottom of the board.
   1. Double check that all of the drivers are firmly seated in the sockets, and that none of the heat sinks shifted during installation.
   1. Mount the CNC Hat on the Arduino. The 12v power connection on the lower left of the hat should be directly above the Arduino power jack also on the lower left.

![Assembled controller boards](/docs/media/rasp_pi2.png){: style="height:30%;width:30%"}
![Assembled controller boards](/docs/media/arduino.png){: style="height:30%;width:30%"}

### Syringe Pump Assembly

#### Syringe pumps parts

- Metal rods
- Nuts
- Syringe pumps - 3D printed from STL file
  - Syringe Plunger holder??
  - Motor base [Part 3D-1]
- Motors
  - BIQU A4988 Compatible StepStick Stepper Motor Diver Module with Heat Sink for 3D Printer Controller Ramps 1.4(Pack of 5pcs)
  - Twotrees Stepper Motor Nema 17 Motor 42BYGH 1.8 Degree Body 38MM 4-Lead Wirel .5A 42N.cm (60oz.in) with 1 m Cable for DIY CNC 3D Printer (Pack of 3)
- Tubing 1/2”?
  - Tubing to syringe pumps into ration chamber
  - Tubing to and from the jacketed portion of the reactor
- Stir motors
- Circulation pump to push fluid

#### Verify Stepper Motor Wires

Before you begin assembling components, it is important to verify that your stepper motors are wired correctly. Each motor will have four different color wires. To verify that the motor is wired in a way that is compatible with the CNC Hat, you need to identify the pairs of wires that feed the two coils inside the motor.

With the motor disconnected, you should be able to spin the shaft with your fingers and feel almost no resistance. Take a short length of wire and jumper the top two pins (Pins 1 and 2) of the connector together. If the motor is wired correctly you should now feel some resistance when you spin the shaft (you should be able to feel the “steps” in the stepper motor). Repeat this procedure with the bottom two pins (Pins 3 and 4). If you do not feel any change in resistance, try jumpering other combinations of pins until you identify the two pairs. It is ESSENTIAL that the top two pins form a pair, and the bottom two pins form a pair, but the order of the wires within each pair does not matter. For example, if you find that pins 1 and 3 are a pair, you will need to rewire the connector so that these two are the top pair, and pins 2 and 4 are the bottom pair.

### ASSEMBLY

1. Assemble the Syringe pumps

   1. Insert the metal rods (part [x]), into the small holes on the [bottom] of the motor base. Insert screw and nuts into the holes nearby, and tighten them down until the metal rods are firmly held in place. The nuts will be placed on the inside of motor base, set into the hexagonal slots for the nuts.

   1. Screw in the Stepper Motor [part x], to the Motor base [Part 3D-1]. The stepper motor is screwed onto the [top].

      1. [note: a lot of these directions are going to reference top and bottom, as though we have made the changes i suggested and labeled the parts so they come out labeled more clearly from the 3d printer. We will need to revisit and expand on this language without the parts being labeled.]
      1. Note: The rods should remain firmly in place, even if bearing the weight of the stepper motor. They should also remain in place if the assembly is turned right-side up and shaken gently.

   1. Cut an approximately 1.5 inch / 4 cm length of silicon tubing (Part [x]), and feed it halfway onto the motor shaft. Leave enough tubing dangling from the motor shaft to attach the threaded rod, later in step [[Double check reference before publication] 7.4.9]
   1. Screw the Syringe Plunger holder (Part [xx]) onto the Carriage. The wide part of the Plunger Holder should face away from the rest of the assembly, resulting in an angled slot that the plunger of the syringe will rest in once assembly is completed.
   1. Set a nut [part (x)] into the slot in the back end of the carriage. There are two slots in the back of the carriage. The nut should fit snugly into the smaller of two holes.
   1. Feed the threaded rod (part [x]) into the slot in the back of the carriage. Feed it into the nut, and screw it in place so the threaded rod travels all the way through the carriage. Turn the threaded rod until the carriage is at least a quarter of a way down the rod, to allow enough exposed guide rods to place the syringe end in place in step [[double check reference before publishing] 7.4.12]
   1. Feed the carriage onto the metal rods. The threaded rod should line up perfectly to the motor shaft of the stepper motor. If it does not line up, remove the carriage assembly, and place it back on the rods facing the other direction.
   1. Attach the Bearing to the Syringe End ’s [top] by snapping the hole on the top side. It should fit snugly.
   1. Place the Syringe Ring over the bearing, and screw into place. The syringe ring will hold the bearing in place. Nuts go into the syringe ring part, in the hexagonal spots provided.
   1. Fit the Syringe End over the threaded rod, and the guide rods. The threaded rod should be able to pass through the entire assembly. The guide rods should fit into slots in the base.
   1. Insert nuts into the hexagonal slots, and screws into the other side. Tighten until the syringe end can hold the weight of the whole assembly when lifted.
   1. Connect the threaded rod to the motor shaft of the stepper motor. You should now have an carridge that will move up and down upon the rod assembly if the threaded rod is turned.

1. Attach Syringe pumps to Arduino
   1. (video part 1: 13:42) Plug the stepper motor connectors into the CNC Hat. Connect one stepper motor to driver Y (upper right) and the other to driver A (lower right). The wire colors on your motors may not match those shown in the video, so simply use the same orientation for both connectors (for example, red wires toward the bottom). If this causes the motors to run backwards it can be corrected later by reversing the connectors (for example, red wires toward the top).
   1. (not shown in video) Cut about 1ft of black 18AWG wire (MC-WIRE), and 1ft of red 18AWG wire, and strip ¼ inch of inch of insulation from one end of each wire, and ½ inch from the other end.
   1. (video part 1: 14:09) Insert the ¼ inch end of the black wire into the negative (-) side of the 12v power supply screw terminal in the lower left corner of CNC Hat. If too much bare wire extends outside the terminal, it is possible for the power connection to short out and create a fire hazard. If necessary, trim the wire to minimize the amount exposed. Tighten the screw with a small flat blade screwdriver to secure the wire in place.
   1. (video part 1: 14:21) Insert the ¼ inch end of the red wire into the positive (+) side of the 12v power supply screw terminal. Again, trim the bare wire if necessary, then tighten the screw to secure the wire in place.

### Reaction Chamber Assembly

**Reaction chamber parts:**

- Mixing paddle
- Mixing motor
- Reactor manifold - 3D printed mason jar lid (manifold?
- Wide mouth quart Mason jars 32oz
- Regular mouth half pint Mason jar 8oz
- Tubing (5mm ?)
- Tubing 8mm?
- Barbed Tee Fittings
- Pump
- Syringes
- 12 volt beverage heater coil

**Assembling the reactor, pumps, and tubing:**

1. Attach mix paddle to reactor lid and motor
   1. (video part 1: 12:40) Insert the mixing paddle (RX-PDL) up through the center hole in the reactor lid (RX-LID) and press it into place in the shaft of the mixing motor (RX-MXM).
1. (video part 1: 13:08) screw the small mason jar (RX-COR) into the reactor lid, then slide the core into the large mason jar (RX-OUT) and screw the reactor lid down.
   (video part 1: 15:02) Fit a coil of 5mm tubing (RX-TB5) to the outlet of each pump. The outlet is the smaller diameter fitting that extends tangentially from the side of the pump. 1. NOTE: The exact size and combination of tubing and fittings you need will be determined by the diameter of the inlet and outlet on the water pumps. Since the circulating system operates at very low pressure you can often make couplings and reducing fittings by sliding smaller diameter tubing inside larger. However, this will depend on the diameter and wall thickness of the tubing you are using. If you have difficulty making up any of the connections, water with a few drops of dish soap can be used as a lubricant.
1. (video part 1: 15:15) Cut approximately 1” of 8mm tubing (RX-TB8) and fit on the inlet of both pumps. The inlet is the larger diameter fitting in line with the major axis of the pump.
1. (video part 1: 16:04) Cut 6” of 5mm tubing from the end of each of the coils.
1. (video part 1: 16:16) Fit one 6” pieces of 5mm tubing to the center stem of each of the barbed tee fittings (RX-TEE)
1. (video part 1: 17:35) Cut approximately 1” of 5mm tubing from the end of each coil.
1. (video part 1: 17:42) Fit each of these 1” pieces inside the 8mm tubing connected to the inlet of each pump.
1. (video part 1: 17:55) Connect both pump inlets to the arms of one of the barbed tee fittings
1. (video part 1: 18:16) Feed the 6” piece of tubing extending from the inlet tee into one of the holes in the reactor lid. Be sure that the tubing is going into the larger outer mason jar and not into the reactor core.
1. (video part 1: 18:30) Connect the other ends of the 5mm tubing coils attached to the pump outlets to the arms of the remaining barbed tee.
1. (video part 1: 18:43) Feed the 6” piece of tubing extending from the outlet tee into one of the holes in the reactor lid. Again, be sure that the tubing is going into the larger outer mason jar and not into the reactor core.
1. (video part 1: 19:35) Cut two lengths of 4mm tubing approximately 12” long. These pieces will connect the syringe pumps to the reactor, so you may need to adjust the length depending on how you have the syringe pumps arranged. The tubing should be as short as practical.
1. (video part 1: 19:40) Attach one end of each tube to each syringe and feed the other end through the hole in the reactor lid leading into the core jar. Be sure the tubing does not prevent the mixing paddle from turning.
1.

## Appendix

### Attachments

Build Video
Operations Guide Link
Support Email Address?

### Reference & Safety

- External References
  - [Open Source Syringe Pump](https://www.appropedia.org/Open-source_syringe_pump) - The Microlab uses a version of this to make the syringe pumps. A few parts are omitted for simplicity.
  - Getting Started with Raspberry Pi - A walkthrough for getting your raspberry pi formatted properly.
- Internal References
  - https://github.com/FourThievesVinegar/solderless-microlab
- Safety Precautions
  - Raw Materials for 3D printing - what is safe to use for the reactor manifold, that will not interact with the materials in the reaction chamber?
  - Electrical mains current runs through the heater coil.
  - GFCI Dongle
- Other Concerns for assembly, but not operation

### Definitions

| Term                         | Definition                                                                                                                                                                                                                                                                                                                                               |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raspberry Pi                 | A type of microcontroller board that is a small computer with the same main parts of a full sized computer, the like central processing unit (CPU), input/output (I/O), memory, and peripherals.                                                                                                                                                         |
| Arduino                      | A development board (programmable circuit board) that is used for many purposes, like accepting inputs from buttons, collecting data from sensors, and controlling motors.                                                                                                                                                                               |
| Controlled Lab Reactor (CLR) | Controlled Lab Reactor or CLR is any reaction system where there is an element of automated control. Generally it refers to a jacketed glass vessel where a circulating chiller unit pumps a thermal control fluid through the jacket to accurately control the temperature of the vessel contents. https://en.wikipedia.org/wiki/Controlled_lab_reactor |
| OS                           | Operating System. This is the central software that runs all other programs. Windows is the most famous example of an Operating System. This project uses Ubuntu, a version of the Linux operating system.                                                                                                                                               |

### Headless Install

- install [raspberry pi imager](https://www.raspberrypi.com/software/)

- install [putty](https://www.putty.org/)

- install [win32diskimager](https://sourceforge.net/projects/win32diskimager/) and backup the your current pi SD card

[001] Get Windows connection sharing working if needed (turn sharing on for WiFi, and select Ethernet adapter connected to the Raspberry Pi as shared) This can be finicky in Windows 10. If you have trouble, try this: turn off sharing for wifi, bridge the Ethernet and wifi (ctrl click WiFi and Ethernet connections, then right click and choose 'Bridge') Wait for the bridge to get established, then disable it, and delete it. Try sharing the WiFi again.

[010]Burn new Raspberry Pi image with default Raspian OS image. [020]The SD card should have two drive letters, one for the boot sector, and one for the main image. [030]Under settings (gear icon) enable ssh, set hostname:microlab, user:ftvc, password:4thieves
[040]Click "Write" to burn the image

[050]Using putty, log in to microlab for the first time, accept the warning about the unknown key.

- If you can't log in to the Pi, you probably forgot to enable SSH. Put the SD card back in the reader on your PC and add an empty file named 'SSH' (with no file extension) to the boot sector. In windows, the easiest way is to right click 'add new text file', then delete the .txt extension once the file is created.

Roughly following the steps from [https://github.com/FourThievesVinegar/solderless-microlab](https://github.com/FourThievesVinegar/solderless-microlab)

Clone the repo

```
$ git clone https://github.com/FourThievesVinegar/solderless-microlab.git
$ cd solderless-microlab
```

[060]Install python dependencies

```
$ sudo apt update
```

NOTE: get some notices about upgradeable packages, is this necessary?

```
$ sudo apt install python3 python3-pip python3-virtualenv
```

NOTE: python-virtualenv is not needed. libfuse2 is no longer required and should be removed

Setup virtual environement and install more dependencies with pip

```
$ cd backend
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

QUESTION: the section "Redis (on the Pi)" doesn't seem to be needed? The test GUI will load without this, but I can't tell if this is necessary for the real thing.
QUESTION: should this be done within the virtualenv, does it matter?

```
(env)$ sudo apt update
(env)$ sudo apt install redis-server
```

[070]Edit redis.conf, change 'supervised no' to 'supervised systemd' > ctrl+x > y (to save) > enter (to overwrite file)

```
(env)$ sudo nano /etc/redis/redis.conf
```

Don't start the server yet, install yarn first.

```
(env)$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
```

[080]WARNING: apt-key is deprecated. Does this line need to be changed?

```
(env)$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
(env)$ sudo apt update
(env)$ sudo apt install yarn

(env)$ sudo nano /solderless-microlab/backend/config.py
change celeryMode = 'real' to celeryMode = 'test'

(env)$ cd gui
(env)$ yarn install
[090]I got some errors, probably due to unstable network connection, took several tries to fetch everything
```

Start the main script, and have it run in the background

```
(env)$ cd ../backend
(env)$ python main.py &

<enter> to get to command line
```

Confirm main.py is still running by checking the list of running scripts

```
(env)$ pgrep -af python
```

NOTE: if you need to stop the script at any point, $ kill -9 <process#>

start the GUI

```
(env)$ cd ../gui
(env)$ yarn start
```

[100]Wait for the server to load, can take several minutes on the Pi 2
[110]Get some warnings about browser lists being outdated
[120]Eventually the server starts with some warnings about missing dependencies

leave the putty session running
[130]In the browser on your pc navigate to microlab:3000 and you should see the microlab interface.

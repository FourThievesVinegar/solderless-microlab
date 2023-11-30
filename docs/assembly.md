# Microlab Assembly

&nbsp;

## Building a Microlab

![Built Microlab](/docs/media/microlab-on-bench.jpg)

The Microlab consists of four major parts:

1. Reactor Unit
1. Reagent Pump Unit
1. Lab Control Unit
1. Temperature Control Unit 

**Reactor Unit**
The central part of the Microlab is the reaction chamber. It consists of a custom 3D printed Mason jar lid (called the reactor manifold) that allows a small mason jar to nest into a larger, wide-mouthed mason jar. During operation, the large mason jar is filled with water. Holes in the mason jar lid allow a pair of pumps to pump in hot or cold water to control the temperature of the water inside the large, outer mason jar. A stir rod with paddle mixes the chemicals in the smaller jar.

**Reagent Pump Unit**
The Microlab uses peristaltic pumps (or 3D printed syringe pumps) to insert additional chemicals into the reaction chamber according to the recipe in progress. These pumps have syringes inserted into them. They are driven by stepper motors that are controlled by the Lab Control Unit.

**Lab Control Unit**
The Lab Control Unit is the brain of the device. It consists of an Arduino microcontroller (a programmable circuit board) and a Raspberry Pi (a mini computer), along with a number of other components.

The Arduino controls the syringe pumps, while the Raspberry Pi runs the software to execute the recipe that the user has selected. The Pi also controls the stirrer and temperature control pumps, monitors the temperature inside the Reaction Unit, and keeps track of the recipe steps.

**Temperature Control Unit**
The Temperature Control Unit powers the heating elements used to maintain temperature in the Reactor Unit. It contains a GFCI outlet, a control relay, and inputs so that the Lab Control Unit can activate it when needed. Because it controls the mains power required to heat the Reactor, it must be carefully constructed.

### Safety

#### Mains Power
The primary safety concern while assembling, testing, and using the Microlab is the mains power used to run the heaters and maintain Reactor temperature. You are a cute bag of mostly water and are weak to electrical damage. Always check your connections during assembly and prior to use. We **HIGHLY** recommend building your Microlab using all safety components, including GFCI outlets, properly-rated relays, an inlet power module with a fuse, and proper grounding. During operation, make sure that all electrical components are kept away from liquids.

#### Chemistry
Chemicals can be dangerous. Make sure you research any reagents, solvents, and other chemicals you work with to ensure you're handling them properly. Always wear appropriate protective equipment and make sure your work area is properly ventilated.

### Materials

![Parts laid out on table](/docs/media/parts_label.png)

Fig. 1 Parts Photo
&nbsp;

### Parts List

&nbsp;
The boards, components and parts needed for this project are located in the Bill of Materials (BOM) file.

Download the BOM here: [https://github.com/FourThievesVinegar/solderless-microlab/blob/master/docs/microlab-parts-list.xlsx](https://github.com/FourThievesVinegar/solderless-microlab/blob/master/docs/microlab-parts-list.xlsx)

### 3D Printed Parts

While most items on the parts list can be purchased, a few items will need to be printed using a 3D printer:

- syringe pumps (unless using peristaltic pumps)
- reactor manifold
- motor mount
- heating vessel lid (unless using hand-modified jar lid)
- cooling vessel lid
- tube fittings (can be purchased, but printed versions are in the parts repo)

Parts files are available here: [https://github.com/FourThievesVinegar/Parts/](https://github.com/FourThievesVinegar/Parts/)

**Syringe pumps**

NOTE: for ease of use and assembly, the syringe pump assembly can be replaced with off-the-shelf peristaltic pumps.

**Quantity: 3**

The syringe pump is made up of 8 parts that must be printed. The parts are labelled Linear Actuator with a part number.
https://www.youmagine.com/designs/syringe-pump

![Syringe pump](/docs/media/syringe_pump2.png)

**Reactor manifold**

**Quantity: 1**

This 3D printed lid allows the smaller jar to nest inside the larger jar of the reaction chamber, [STL available here](https://github.com/FourThievesVinegar/Parts/blob/master/v4/reactorManifold_v0.7.STL).


**Mixing motor mount**
NOTE: This part and assembly is still under active development and is subject to re-designs.

**Quantity: 1**

This part attaches to the manifold and holds the mixing motor, which is coupled to the mixing paddle. 

**Inspect 3D printed part**
Before assembly, be sure to inspect the parts that have come out of the 3D printer.

1. Ensure the inner reactor (part [x]) and outer reactor (part [y]) can be screwed into the Reactor Manifold (Part 3D [xx]).
1. Check to make sure all screw holes are open. Use a drill to clear them if needed
1. Check to make sure the holes on the [center part] are open to allow guide rods and the threaded rod to pass thru. Use a drill to clear them of excess print material if needed.

## Instructions

### Lab Control Unit Assembly

![Assembled controller boards](/docs/media/controller_boards.png)

#### Electronic Parts:

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
   1. (Not shown in video) Mount the heat sinks on the motor control drivers (MC-MDR) with thermal adhesive, making sure that the heat sink does not contact any of the pins.
   1. (video part 1: 00:18 WARNING: video incorrectly shows installing all 4 drivers) Mount the motor control drivers (MC-MDR) on the CNC hat (MC-CNC). The four drivers are labeled X, Y, Z, and A. Since this project only requires three stepper motors, we will only use sockets X, Y, and Z. To ensure you have the orientation correct, orient the CNC hat so that the 12v power connection is in the lower left, the reset button is in the upper left. Orient each of the A4988 drivers so that the small potentiometer (looks like a small phillips head screw) is toward the bottom of the board.
   1. Double check that all of the drivers are firmly seated in the sockets, and that none of the heat sinks shifted during installation.
   1. Mount the CNC Hat on the Arduino. The 12v power connection on the lower left of the hat should be directly above the Arduino power jack also on the lower left.

![Assembled controller boards](/docs/media/rasp_pi2.png)
![Assembled controller boards](/docs/media/arduino.png)

#### Lab Control Unit Housing assembly

With the release of version 0.5 of the Microlab, we recommend enclosing the Lab Control Units in an enclosure that provides protection to the components and standard interfaces to the other units. This enclosure can be produced using corrugated plastic or another material that you are comfortable cutting and shaping into a box. Because folded corrugated plastic tends to return to its original position, it may be necessary to cut off tabs and re-attach them with duct tape, which provides more flexibility. The pictured enclosure is 8" x 6" x 4" and fits all of the Lab Control Unit components comfortably inside. We also recommend a small fan to ensure air flow. Components and velcro straps can be attached to the enclosure using short M3 screws, washers, and nuts.

**Cutting the housing**

- Cut a hole for the display (take care measuring so that the hole fits the screen as closely as possible). 
- Cut holes for the cables, the barrel plug connectors (if using them), and the button for the light (if using it)
- We also recommend cutting holes for a fan to prevent overheating

![Control Unit Exterior](/docs/media/microlab-control-unit.jpg)

The Lab Control Unit enclosure is designed to be as modular as possible. In this image, the cables for the Reagent Pump Unit and thermistor are fixed, but cables for the circulation pumps, reaction chamber light, mixing motor, and Temperature Control Unit provide standard interfaces for cables. The knob is an optional PWM motor speed controller that allows manual control over the mixing motor's speed.

![Control Unit Interfaces](/docs/media/microlab-control-unit-interface.jpg)

**Mounting the components**

- Inside the enclosure, connect the 5v and 12v power supplies to the enclosure with velcro straps. 
- Attach the straps to the case using small M3 screws. 
   - You can use similar screws to connect the larger lever connectors, the arduino, and the relay break-out board (if you are using it instead of the Pi hat). 
   - You can use similar straps to hold the display and the Pi in place.
   - Basically, everything is going to be strapped in and bolted down
   - You can also attach small velcro straps to bundle wires and reduce the rats nest factor

The interface to the other components are standard female barrel plug connectors.
- Insert the leads for these through the holes you cut previously 
   - Cut away any excess housing material on the threads
   - Secure to the enclosure with the connectors' threaded nuts
- Use lever connectors as needed to connect the leads from the barrel plug connectors to the 12v power, as well as to the appropriate relays.
   - If you're not sure which relays are which, consult the documentation for your relay hat or board.
   - Consult the pin diagram for your Pi for which GPIO pins to connect to the relay board if you are using a separate relay breakout board like the one pictured here.
   - See `backend/hardware/base_hardware.yaml` for which GPIO pins activate which systems
- If you have a reactor light and a button to use it with, wire the button according to its instructions and connect it to the appropriate barrel plug connector.

There are several other connections to make inside the housing:
- Connect the 12v input on the Arduino's motor control board to the 12v power supply
- Connect the temperature probe and motor control shield to the USB ports on the Pi. You may also want to add a short male-to-female USB cable to more easily connect to peripherals like a keyboard.
- The relay board and fan both require 5v power. Set up a 1-to-3 lever connector to use as a splitter and connect them to it
   - As input, you can use the +5v and GND from the motor control shield
- Connect the stepper motor control cables to the motor control board
   - Wrap the 3 stepper motor control cables in the split loom cable wrap
      - We highly recommend you label both ends of the cables with tape!
   - Feed the 4-wide end of the cables (not the 6-wide - those plug into the motors!) and the cable wrap into the housing
   - Connect each of the X, Y, and Z cables to the appropriate spot on the motor control board
   - Secure the cables inside the cable wrap (tight zip ties are good for this) and secure the cable wrap to the enclosure using copius electrical tape
      - The goal is to prevent cables from being yanked loose or damaging components when tugged from the outside

Once everything is connected, the inside of your box should look something like this:

![Control Unit Interior](/docs/media/microlab-control-unit-inside.jpg)

NOTE: In this image, the relay board is separated from the Pi (rather than using a relay hat). It is possible to wire everything together using less-expensive soldering techniques or wire nuts, but the lever connectors are very easy to assemble and reconfigure as needed.

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
  - Tubing to syringe pumps into ration chamber (peristaltic pumps will come with their own tubing)

#### Verify Stepper Motor Wires

Before you begin assembling components, it is important to verify that your stepper motors are wired correctly. Each motor will have four different color wires. To verify that the motor is wired in a way that is compatible with the CNC Hat, you need to identify the pairs of wires that feed the two coils inside the motor. **It is likely that the cables that came with the stepper motors will *just work* but verification is still worthwhile**

With the motor disconnected, you should be able to spin the shaft with your fingers and feel almost no resistance. Take a short length of wire and jumper the top two pins (Pins 1 and 2) of the connector together. If the motor is wired correctly you should now feel some resistance when you spin the shaft (you should be able to feel the “steps” in the stepper motor). Repeat this procedure with the bottom two pins (Pins 3 and 4). If you do not feel any change in resistance, try jumpering other combinations of pins until you identify the two pairs. It is ESSENTIAL that the top two pins form a pair, and the bottom two pins form a pair, but the order of the wires within each pair does not matter. For example, if you find that pins 1 and 3 are a pair, you will need to rewire the connector so that these two are the top pair, and pins 2 and 4 are the bottom pair.

#### ASSEMBLY

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
1. Tuning potentiometers: **WARNING!** Failure to correctly tune the potentometers can damage the motor controller and the motors themselves. To tune them, **gently** turn the potentometers clockwise using a small phillips head screw driver, taking care not to turn past any resistance. Turning them clockwise "closes" the voltage down while turning them counter-clockwise "opens" the voltage up. Start with the potentiometers in the "closed" position, and slowly "open" each of them a quarter of a turn at a time until the stepper motors respond correctly - they should turn smoothly. If they do not move, "open" the potentometer a quarter turn and try again. If they move erratically, your voltage is likely too high and you may have damaged the board or the motors. The Microlab comes with a Test Recipe that can be used to test the reagent pump motors.

### Reactor Unit Assembly

![Assembled Reactor Unit](/docs/media/microlab-reactor-unit-pump-unit-assembled.jpg)
![Assembled Reactor Unit rear](/docs/media/microlab-reactor-unit-pump-unit-assembled-rear.jpg)

**Reactor Unit parts:**

- Mixing paddle
- Mixing motor
- Reactor manifold - 3D printed mason jar lid
- Wide mouth quart Mason jar 32oz
- Regular mouth half pint Mason jar 6oz
- Tubing (5mm / 8mm) - use tubing compatible with your circulation pumps
- Barbed Tee Fittings
- Housing walls, corner reinforcements, and straps

**Assembling the reactor, pumps, and tubing:**

1. Attach mix paddle to reactor lid and motor
   1. (video part 1: 12:40) Insert the mixing paddle (RX-PDL) up through the center hole in the reactor lid (RX-LID) and press it into place in the shaft of the mixing motor (RX-MXM).
   1. You will likely need a coupler for this. You can use surgical tubing to connect the mixing paddle shaft to the motor coupling. This component is still being refined as the current design is not optimal.
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

#### Reactor Unit Housing Assembly

**Reactor Unit Housing parts:**

- 5 pieces thin plywood, cut to 8" x 8"
- Corner reinforcements 
   - We used upcycled protective corners from a shipping package 
   - Any three-corner joining hardware will work, but these are convenient with the velcro straps and allow rapid assembly and breakdown
- Light strip
- Adhesive-backed velcro patches
- Two-sided velcro to cut straps from

**Reactor Unit Housing assembly:**

- Cut and paint plywood
   - Depending on your corner reinforcements, you may want a different method than we used here. We intend these units to pack mostly flat for storage and shipping.
   - For this, we drilled 1/2" holes large enough for the 
   - The top face should have a hole cut just large enough to fit the top of the large mason jar through. A 3d-printed collar that securely holds the jar in place can be found in the Parts repository [https://github.com/FourThievesVinegar/Parts/tree/master/v5](https://github.com/FourThievesVinegar/Parts/tree/master/v5)
- Cut velcro straps
   - 4 long straps (~16") for the back corners (they join 3 faces of the housing)
   - 4 short straps (~6") for the front corners (they join 2 faces of the housing)
- Cut, paint, and assemble reactor housing door (use packing tape for the transparent door)
   - Use the long velcro straps to weave 
   - This unit uses sticky velcro patches to hold the door to the rest of the assembly
- Attach light strips to the inside of the top face of the housing
   - We used 12v LED strips stuck to a scrap of corrugated plastic, which attaches to the housing with adhesive velcro patches

![Reactor housing assembly 2](/docs/media/reactor-housing-assembly-2.png)

![Reactor housing assembly 3](/docs/media/reactor-housing-assembly-3.png)

![Reactor housing assembly 4](/docs/media/reactor-housing-assembly-4.png)

### Temperature Control Unit Assembly

![Temperature Control Unit](/docs/media/microlab-temperature-control-unit.jpg)

**Temperature Control Unit Parts**
- Circulation Pumps
- Tubing to and from the jacketed portion of the reactor
- Beverage heater coil (2 recommended for faster heating)
- 2-Gang electrical box and face plate
- GFCI Outlet
- 6oz Canning jar (NOTE: Using a larger jar with the pumps submerged inside may be preferable for priming, but submerging the pumps has impacts on their heat tolerances)
- Relay (Must support mains power!)
- Inlet power module with fuse
- Quick disconnect electrical connectors
- AC power cord

#### Assembly
- Connect the inlet power module to the GFCI outlet with the relay between them (it doesn't matter whether the relay is on the positive or negative side)
   - NOTE: Carefully consult the wiring instructions for the Inlet and be familiar with basic safety and wiring with mains power. We cannot stress enough that this is the most dangerous part of the Microlab itself. We highly recommend that you cover all exposed terminals with electrical tape and wrap it thorouthly.
   - Use the quick disconnect connectors.
- Connect the GFCI ground to the Inlet's ground connection.
- Put it all in the 2-gang electrical housing.
   - Screw the GFCI outlet securely into the housing
   - Cut a hole in a decora blank to fit the power inlet and drill smaller holes to allow your three wire connector's leads inside the box.
   - Attach the power inlet to the blank securely by drilling through the blank/decora plate. Use small M3 screws.
- Connect the relay to the positive, negative, and signal wires on your three-wire connector. Wrap a zip tie or copius electrical tape around the leads to prevent them from getting yanked and disconnecting.
- Screw the 2-gang plate onto the 2-gang housing

**TODO: Photos**

## Appendix

### Attachments

Build Video
Operations Guide Link
Support Email Address?

### References

- External References
  - [Open Source Syringe Pump](https://www.appropedia.org/Open-source_syringe_pump) - The Microlab can use a version of this for the syringe pumps. A few parts are omitted for simplicity. Even simpler is to use peristaltic pumps driven by stepper motors, which require almost no assembly.
  - Getting Started with Raspberry Pi - A walkthrough for getting your raspberry pi formatted properly.

### Definitions

| Term                         | Definition                                                                                                                                                                                                                                                                                                                                               |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raspberry Pi                 | A type of microcontroller board that is a small computer with the same main parts of a full sized computer, the like central processing unit (CPU), input/output (I/O), memory, and peripherals.                                                                                                                                                         |
| Arduino                      | A development board (programmable circuit board) that is used for many purposes, like accepting inputs from buttons, collecting data from sensors, and controlling motors.                                                                                                                                                                               |
| Controlled Lab Reactor (CLR) | Controlled Lab Reactor or CLR is any reaction system where there is an element of automated control. Generally it refers to a jacketed glass vessel where a circulating chiller unit pumps a thermal control fluid through the jacket to accurately control the temperature of the vessel contents. https://en.wikipedia.org/wiki/Controlled_lab_reactor |
| OS                           | Operating System. This is the central software that runs all other programs. Windows is the most famous example of an Operating System. This project uses Ubuntu, a version of the Linux operating system.                                                                                                                                               |

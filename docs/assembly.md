# Microlab Assembly

&nbsp;

## Building a Microlab

![Built Microlab](/docs/media/microlab-on-bench-labeled.jpg)

The Microlab consists of four major parts:

1. Reactor Unit
1. Reagent Pump Unit
1. Lab Control Unit
1. Temperature Control Unit 

**Reactor Unit**
The central part of the Microlab is the reaction chamber. It consists of a custom 3D printed Mason jar lid (called the reactor manifold) that allows a small mason jar to nest into a larger, wide-mouthed mason jar. During operation, the large mason jar is partly filled with water. Holes in the mason jar lid allow a circulation pump to pump in hot or cold water to control the temperature inside the large, outer mason jar. A stir rod with paddle mixes the chemicals in the smaller jar.

**Reagent Pump Unit**
The Microlab uses peristaltic pumps (or 3D printed syringe pumps) to insert additional chemicals into the reaction chamber according to the recipe in progress. These pumps have syringes inserted into them. In both cases, they are driven by stepper motors that are controlled by the Lab Control Unit.

**Lab Control Unit**
The Lab Control Unit is the brain of the device. It consists of an Arduino microcontroller (a programmable circuit board) and a Raspberry Pi (a mini computer), along with a number of other components.

The Arduino controls the syringe pumps, while the Raspberry Pi runs the software to execute the recipe that the user has selected. The Pi also controls the stirrer and temperature control pumps, monitors the temperature inside the Reaction Unit, and keeps track of the recipe steps.

**Temperature Control Unit**
The Temperature Control Unit contains the heating elements used to maintain temperature in the Reactor Unit. It has a power block that is composed of a GFCI outlet, a control relay, and inputs so that the Lab Control Unit can activate it when needed. It also has a heat exchanger composed of a jar containing water, a coil of copper tubing, and beverage heaters. Because the heating elements run on mains power, the Temperature Control Unit must be carefully constructed.

### Safety

#### Mains Power
The primary safety concern while assembling, testing, and using the Microlab is the mains power used to run the heaters and maintain Reactor temperature. You are a cute bag of mostly water and are weak to electrical damage. Always check your connections during assembly and prior to use. We **HIGHLY** recommend building your Microlab using all safety components, including GFCI outlets, properly-rated relays, an inlet power module with a fuse, and proper grounding. During operation, make sure that all electrical components are kept away from liquids.

#### Chemistry
Chemicals can be dangerous. Make sure you research any reagents, solvents, and other chemicals you work with to ensure you're handling them properly. Always wear appropriate protective equipment and make sure your work area is properly ventilated.

### Materials

![Parts laid out on table](/docs/media/parts_label.png)

Fig. 1 Parts Photo showing printed syringe parts

### Parts List

The boards, components and parts needed for this project are located in the Bill of Materials (BOM) file.

Download the BOM here: [https://github.com/FourThievesVinegar/solderless-microlab/blob/master/docs/microlab-parts-list.xlsx](https://github.com/FourThievesVinegar/solderless-microlab/blob/master/docs/microlab-parts-list.xlsx)

### 3D Printed Parts

While most items on the parts list can be purchased, a few items will need to be printed using a 3D printer:

- syringe pump components (unless using peristaltic pumps)
- reactor manifold
- motor mount
- heating vessel lid (unless using hand-modified jar lid)
- cooling vessel lid (unless using a hand-modified jar lid)
- tube fittings (can be purchased, but printed versions are in the parts repo)

Parts files are available here: [https://github.com/FourThievesVinegar/Parts/](https://github.com/FourThievesVinegar/Parts/)

#### Syringe pumps

NOTE: for ease of use and assembly, the syringe pump assembly can be replaced with off-the-shelf peristaltic pumps.

**Quantity: 3**

#### Reactor manifold

**Quantity: 1**

This 3D printed lid allows the smaller jar to nest inside the larger jar of the reaction chamber, [STL available here](https://github.com/FourThievesVinegar/Parts/blob/master/v4/reactorManifold_v0.7.STL).


#### Mixing motor mount
NOTE: This part and assembly is still under active development and is subject to re-designs.

**Quantity: 1**

This part attaches to the manifold and holds the mixing motor, which is coupled to the mixing paddle. 

#### Inspect 3D printed parts
Before assembly, be sure to inspect the parts that have come out of the 3D printer.

1. Ensure the inner reactor (part [x]) and outer reactor (part [y]) can be screwed into the Reactor Manifold (Part 3D [xx]).
1. Check to make sure all screw holes are open. Use a drill to clear them if needed
1. Check to make sure the holes on the [center part] of the syringe pumps are open to allow guide rods and the threaded rod to pass thru. Use a drill to clear them of excess print material if needed.

## Instructions

### Lab Control Unit assembly

Assembling the Lab Control Unit involves assembling and wiring several electronic components of the Microlab. 

For full instructions, see [Microlab Lab Control Unit Assembly](/docs/assembly-lab-control-unit.md).

### Syringe Pump assembly

Assembling the syringe pumps is done one of two ways, depending on whether you have opted for 3d-printed linear syringe pumps or off-the-shelf peristaltic pumps.

For linear syringe pumps, see [Linear Syringe Pump Assembly](/docs/assembly-syringe-pumps.md)
For peristaltic pumps, see [Peristaltic Pump Assembly](/docs/assembly-peristaltic-pumps.md)

#### Verify stepper motor wires and tune the potentiometers

##### Stepper motor verification
Before you run the Microlab, it is important to verify that your stepper motors are wired correctly and that your control board is calibrated. Each motor will have four different color wires. To verify that the motor is wired in a way that is compatible with the CNC Hat, you need to identify the pairs of wires that feed the two coils inside the motor. **It is likely that the cables that came with the stepper motors will *just work* but verification is still worthwhile**

With the motor disconnected, you should be able to spin the shaft with your fingers and feel almost no resistance. Take a short length of wire and jumper the top two pins (Pins 1 and 2) of the connector together. If the motor is wired correctly you should now feel some resistance when you spin the shaft (you should be able to feel the “steps” in the stepper motor). Repeat this procedure with the bottom two pins (Pins 3 and 4). If you do not feel any change in resistance, try jumpering other combinations of pins until you identify the two pairs. It is ESSENTIAL that the top two pins form a pair, and the bottom two pins form a pair, but the order of the wires within each pair does not matter. For example, if you find that pins 1 and 3 are a pair, you will need to rewire the connector so that these two are the top pair, and pins 2 and 4 are the bottom pair.

##### Motor board potentiometer tuning
Once you have verified the wiring, you can tune the potentiometers on the motor control board.

**WARNING!** Failure to correctly tune the potentometers can damage the motor controller and the motors themselves. To tune them, **gently** turn the potentometers on the motor control boards clockwise using a small phillips head screw driver, taking care not to turn past any resistance. Turning them clockwise "closes" the voltage down while turning them counter-clockwise "opens" the voltage up. Start with the potentiometers in the "closed" position, and slowly "open" each of them a quarter of a turn at a time until the stepper motors respond correctly - they should turn smoothly. If they do not move, "open" the potentometer a quarter turn and try again. If they move erratically, your voltage is likely too high and you may have damaged the board or the motors. The Microlab comes with a Test Recipe that can be used to test the reagent pump motors.

### Reactor Unit assembly

Assembling the reactor unit involves two major steps: assembling the Reactor Unit housing and assembling the Reactor Unit itself. 

For full instructions, see [Microlab Reactor Unit Assembly](/docs/assembly-reactor-unit.md).

### Temperature Control Unit assembly

Assembling the Temperature Control Unit involves assembling its two main components: The Power Box and the Heat Exchanger. 

For full instructions, see [Microlab Temperature Control Unit Assembly](/docs/assembly-temperature-control-unit.md)

### Putting it all together

Once you have assembled the 4 major components, you will have what you need to run the Microlab. These components are designed to be modular and easy to disassemble for storage and transportation. It is likely that you will want to at least partly break down the Microlab when not in use. 

For full assembly instructions, see [Microlab Operation](/docs/operation.md).

## Appendix

### References

External References:
- [Open Source Syringe Pump](https://www.appropedia.org/Open-source_syringe_pump) - The Microlab can use a version of this for the syringe pumps. A few parts are omitted for simplicity. Even simpler is to use peristaltic pumps driven by stepper motors, which require almost no assembly.

### Definitions

| Term                         | Definition                                                                                                                                                                                                                                                                                                                                               |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raspberry Pi                 | A type of microcontroller board that is a small computer with the same main parts of a full sized computer, the like central processing unit (CPU), input/output (I/O), memory, and peripherals.                                                                                                                                                         |
| Arduino                      | A development board (programmable circuit board) that is used for many purposes, like accepting inputs from buttons, collecting data from sensors, and controlling motors.                                                                                                                                                                               |
| Controlled Lab Reactor (CLR) | Controlled Lab Reactor or CLR is any reaction system where there is an element of automated control. Generally it refers to a jacketed glass vessel where a circulating chiller unit pumps a thermal control fluid through the jacket to accurately control the temperature of the vessel contents. https://en.wikipedia.org/wiki/Controlled_lab_reactor |
| OS                           | Operating System. This is the central software that runs all other programs. Windows is the most famous example of an Operating System. This project uses Ubuntu, a version of the Linux operating system.                                                                                                                                               |

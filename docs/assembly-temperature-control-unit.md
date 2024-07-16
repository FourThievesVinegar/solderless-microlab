# Heating and Cooling Units Assembly

The Heating Unit and Cooling Units are supporting components of the MicroLab that heat or cool the fluids that circulate in the Reactor Core.

(We are looking into upcycling heat sinks from old computers but are still experimenting - please reach out if you have done this or have suggestions)

<IMG ALT="Temperature Units as raw parts" SRC="./media/reactor-unit/reactor-unit-assembled.jpg" WIDTH="400" />
<IMG ALT="Temperature Units fully assembled" SRC="./media/reactor-unit/reactor-unit-assembled.jpg" WIDTH="400" />

## Skills Needed

* Bending copper tubing


## Tools Needed

* Copper tube jig - for bending the copper (optional but recommended).
    - Various jig options include
      - cylinder of appropriate size
      - Medium-to-large dowel or other sturdy tube
      - the Reactor Core manifold, as it is approximately the correct size. We opened [an issue about this](https://github.com/FourThievesVinegar/solderless-microlab/issues/136)
    - Be careful when bending! Copper tubing kinks easily, reducing flow in both the liquid throughput and "vibes" senses.
    - You can also use a long spring around the tube to support it or fill it with salt or sand to support from the inside.
* Tube cutters - very helpful for neatly cutting the copper tubing without crushing it.



## Parts

| Section | Part ID      | Part Name     | Count | Notes |
|--- | ------------- | ------------- |------| ----|  
|||
|TEMPERATURE CONTROL UNIT|
TC-PMP|Circulating pump|2
TC-SBH|Submersible heater|1
TC-CTB|"Copper tubing 1/4"" OD x 3/16"" ID"|1
TC-STB|Silicone tubing 7mm OD x 5mm ID|1
RX-TEE|Barbed tee fittings for 6mm tubing|2
TC-JAR|32oz canning jar |2
TC-REL|Switchable power supply|1
TC-COZ|Coozie|2
MC-ECD|Extension cord (optional)|1
||


### Purchased

- Copper tubing
- Large mason jar (32oz or larger)
- Large mason jar (16oz or 32oz - we are still determining optimal designs for the heat exchanger)
- Silicone tubing for connecting to the Pumps Box and Reactor Core
- Insulating material (optional, but highly recommended)

### Printed

- Heating Unit lid
- Cooling Unit lid

## Assembly

### Heat Exchanger

This component heats and stores hot water used to heat the Reactor Core.

**Parts:**

- Large Mason Jar (16oz or 32oz - we are still determining optimal designs for the heat exchanger)
- 5 - 10' of copper tubing
  - Alternatives: Other heat exchangers may be used such as a larger home-brewing copper coil or an aluminum transmission oil cooler.
- Printed Heating Unit lid

**Assembly:**

#### Heating Unit

- Bend copper tubing into a helix that will fit in the heat exchanger jar while still leaving space for the heating coils.
 - As a general rule, the more copper tubing you can fit, the more heat will be exchanged.
  - It is OK (good even!) if the copper tubing and heating coils touch.

- Use the 3D printed hot jar lid. Insert the ends of your copper tube helix up through the holes in the lid.
- Insert the heating coil on the heater through the rectangular hole in the top, then twist it 90 degrees so that the top fits snugly in the slot in the jar lid.
  - You may need to cut off a hook or tab meant to hold the heater to the side of a mug.
- Attach to the jar with a standard canning jar lid ring.

### Cooling Unit

This component holds ice water or another cold substance to cool the reactor core.

**Parts:**

- Large Mason Jar (32oz or larger - a bigger jar means more thermal mass)
  - If you bought a pre-formed copper coil, you will need to find a container that fits it.
- 5 - 10' of copper tubing (still experimenting with optimal configurations)
- Printed Cooling Unit lid

**Assembly:**

- Bend copper tubing into a helix that will fit in the jar.
- Use the 3D printed cold jar lid. Insert the ends of your copper tube helix up through the holes in the lid.
- Attach to the jar with a standard canning jar lid ring.

### Connecting Things

Attach silicone tubing to the circulation pumps and to the intake and exhaust of the coiled copper tubing. Run the open ends into the outer jar of the Reactor Core. Make sure they will reach below the water level there.

For more on this, see [MicroLab Operation](/docs/operation.md).



This concludes the assembly instructions for the Heating and Cooling Units. Next up: [Building the Reactor Unit](/docs/assembly-reactor-unit.md)

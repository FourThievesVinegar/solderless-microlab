# MicroLab Temperature Control Units Assembly

Ths Temperature Control Units are auxilary components of the MicroLab that heat or cool the fluids that circulate in the Reactor Core.

<IMG ALT="Temperature Control Units as raw parts" SRC="./media/reactor-unit/reactor-unit-assembled.jpg" WIDTH="400" />
<IMG ALT="Temperature Control Units fully assembled" SRC="./media/reactor-unit/reactor-unit-assembled.jpg" WIDTH="400" />

## Tools Required

- While not strictly required, a tube cutter can be very helpful for neatly cutting the copper tubing without crushing it, which would impede flow. A metal saw will also work.
- A jig for bending the copper (optional but recommended). The Reactor Manifold can be used in a pinch.

## Parts

### Purchased

- Copper tubing (We are looking into upcycling heat sinks from old computers but are still experimenting - please reach out if you have done this or have suggestions)
- Large mason jar (32oz or larger)
- Large mason jar (16oz or 32oz - we are still determining optimal designs for the heat exchanger)
- Silicone tubing for connecting to Pumps Unit and Reactor Core
- Insulating material (optional, but highly recommended)

### Printed

- Heating Unit lid
- Cooling Unit lid

## Assembly

### Heat Exchanger

This component heats and stores hot water used to heat the Reactor Core.

**Components:**

- Large Mason Jar (16oz or 32oz - we are still determining optimal designs for the heat exchanger)
- 5 - 10' of copper tubing (still experimenting with optimal configurations)
- Printed Heating Unit lid

**Assembly:**

- Bend copper tubing into a helix that will fit in the heat exchanger jar while still leaving space for the heating coils.
  - A cylinder of appropriate size might be useful as a jig. In a pinch, you can bend the tubing aroundthe Reactor Core manifold, as it is approximately the correct size. There is [an issue about this](https://github.com/FourThievesVinegar/solderless-microlab/issues/136) on our github.
  - It is OK (good even!) if the copper tubing and heating coils touch.
  - As a general rule, the more copper tubing you can fit, the more heat will be exchanged.
  - Working with the copper:
    - Professionals who work with copper pipe typically have cutters and bending tools.
      - These aren't strictly necessary but they're super-helpful, especially the tube cutter, which makes an even cut without smooshing the tube.
    - Be careful when bending! Copper tubing kinks easily, reducing flow in both the liquid throughput and "vibes" senses.
    - You can use a medium-to-large dowel or other sturdy tube as a jig for bending
    - You can also use a long spring around the tube to support it or fill it with salt or sand to support from the inside.
- Use the 3D printed hot jar lid. Insert the ends of your copper tube helix up through the holes in the lid.
- Insert the heating coil on the heater through the rectangular hole in the top, then twist it 90 degrees so that the top fits snugly in the slot in the jar lid.
  - You may need to cut off a hook or tab meant to hold the heater to the side of a mug.
- Attach to the jar with a standard canning jar lid ring.

### Cold Exchanger

This component holds ice water or another cold substance to cool the reactor core.

**Components:**

- Large Mason Jar (32oz or larger - a bigger jar means more thermal mass)
- 5 - 10' of copper tubing (still experimenting with optimal configurations)
- Printed Cooling Unit lid

**Assembly:**

- Bend copper tubing into a helix that will fit in the jar.
- Use the 3D printed cold jar lid. Insert the ends of your copper tube helix up through the holes in the lid.
- Attach to the jar with a standard canning jar lid ring.

### Connecting Things

Attach silicone tubing to the circulation pumps and to the intake and exhaust of the coiled copper tubing. Run the open ends into the outter jar of the Reactor Unit. Make sure they will reach below the water level there.

For more on this, see [MicroLab Operation](/docs/operation.md).

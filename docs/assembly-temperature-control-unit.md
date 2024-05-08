# MicroLab Temperature Control Unit Assembly

![Temperature Control Unit](/docs/media/microlab-temperature-control-unit.jpg)

## Temperature Control Unit parts
### Heat Exchanger:
- Circulation Pump(s) 
    - NOTE: We highly recommend a single self-priming pump with a high temperature tolerance!
- Copper tubing (1/4" OD x 3/16" ID)
    - The copper tubing OD should be slightly larger than the silicone tubing ID such that the silicone stretches and seals when the copper is inserted.
- Silicone tubing (7mm OD x 5mm ID) to and from the jacketed portion of the reactor
    - We recommend this size because it fits into the Reactor Unit core easily. Larger tubing can get stuck.
- Beverage heater coil (2 recommended for faster heating)
- 16oz Wide-mouth canning jar
    - A 32oz jar (or larger!) may be preferable for cooling as it allows more thermal mass
- An insulating jackets that fits your jars (one may also be desired for the Reactor Unit core)
    - NOTE: We have used various winter hats and coozies for different jars. Knitting / crochet patterns for various standard jars would be welcome!

### Power Box:
- 2-Gang electrical box and face plate
- GFCI Outlet
- Relay (Must support mains power!)
- Inlet power module with fuse
- Quick disconnect electrical connectors
- AC power cord

## Assembly
The Temperature Control Unit has two major parts: The Power Box and the Heat Exchanger. 

### Power Box

*PLEASE NOTE*: We found (and **highly** recommend using) an [off-the-shelf](https://www.amazon.com/Iot-Relay-Enclosed-High-Power-Raspberry/dp/B00WV7GMA2/) solution for this. Docs and parts list will be updated in the next release to reflect this.

![Temperature Control Unit power box](/docs/media/microlab-power-box.jpg)

- Wire the inlet power module and insert the fuse according to manufacturer instructions
- Connect the inlet power module to the GFCI outlet with the relay between them (it doesn't matter whether the relay is on the positive or negative side)
   - NOTE: Carefully consult the wiring instructions for the inlet and be familiar with basic safety and wiring with mains power. We cannot stress enough that this is the most dangerous part of the MicroLab itself and that you are weak to electrical damage. We **highly** recommend that you cover all exposed terminals with electrical tape and wrap it thorouthly.
   - Use the quick disconnect connectors.
- Connect the GFCI ground to the Inlet's ground connection.
- Put it all in the 2-gang electrical housing.
   - Screw the GFCI outlet securely into the housing.
   - Cut a hole in a decora blank to fit the power inlet.
   - Attach the power inlet to the blank securely by drilling through the blank/decora plate. Use small M3 screws.
   - Drill 3 small holes to allow your three wire connector's leads inside the box.
   - Thread the three-wire connector's wires through the holes you drilled.
- Connect the relay to the positive, negative, and signal wires on your three-wire connector. Wrap a zip tie and/or copius electrical tape around the leads to prevent them from getting yanked and disconnecting.
- Screw the 2-gang plate onto the 2-gang housing


### Heat Exchanger

![Temperature Control Unit heat exchanger](/docs/media/microlab-heat-exchanger.jpg)

- Use the 3D printed hot jar lid or cut a standard metal jar lid with the following:
    - Two round holes: one for the intake and one for the exhaust tube.
    - One rectangular hole cut on three sides: this holds the heating coils to the lid. 
        - You can cut the hole using a punch or chisel on a scrap wood block (or however you prefer).
        - Leave the flap from this hole, then cut a smaller slot or rectangular hole in the flap. Use the remainder of the flap as a strap to hold the heaters in place
    - Be careful of sharp edges if you are cutting metal! Fold them as flat as possible and always bend corners back to avoid sharp points that may cut you or future users! Human skin is only slightly resistant to slashing and piercing damage.
- Bend copper tubing into a helix that will fit in the heat exchanger jar while still leaving space for the heating coils.
    - We found it easiest to wrap the copper around the heating could themselves. A tube of the appropriate size might be useful as a jig. There is [an issue about this](https://github.com/FourThievesVinegar/solderless-microlab/issues/136) on our github.
    - It is OK (good even!) if the copper tubing and heating coils touch.
    - The more copper tubing you can fit, the more heat will be exchanged.
    - Working with the copper:
        - Professionals who work with copper pipe typically have cutters and bending tools. 
            - These aren't strictly necessary but they're super-helpful.
        - Be careful when bending! Copper tubing kinks easily, reducing flow in both the liquid throughput and "vibes" sense.
        - You can use a medium-to-large dowel or other sturdy tube as a jig for bending
        - You can also use a long spring around the tube to support it or fill it with salt or sand to support from the inside.
- Attach silicone tubing to the circulation pump and to the intake and exhaust of the coiled copper tubing. Run the open ends into the outter jar of the Reactor Unit. Make sure they will reach below the water level there.
- To use both heating and cooling without changing the hardware configuration between recipe steps, you will need to produce an additional heat exchanger unit for cooling.
    - The cooling unit will not require an additional power box - it is just an ice bath.
    - It will require an additional jar lid, jar, copper coil, pump, and insulating jacket. 

## Notes

- Some of the documents in this repo contain older pictures of the heat exchanger with a 6oz jar. We recommend a 16oz jar to accomodate the copper tubing. 

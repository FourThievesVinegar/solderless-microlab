# Pumps Unit Assembly

The Pumps Unit contains both the pumps that inject reagents into the Reactor Core as well as the pumps that circulate hot and cold fluids to control the Reactor Core's Temperature. It also has plugs for the stirring motor and the Reactor Stand's optional light.

<IMG ALT="Pumps Unit Front showing three peristaltic pumps and two female barrel connectors on the front of a 7 inch by 7 inch 3d printed box" SRC="./media/pumps-unit/pumps-unit-complete-front.jpg" WIDTH="400" />
<IMG ALT="Pumps Unit Rear showing two phoenix connector sockets and screws at the corners." SRC="./media/pumps-unit/pumps-unit-complete-rear.jpg" WIDTH="400" />

## Tools required

- Small screwdrivers for M3 screws
- Wire cutters and strippers

## Parts

### Purchased Parts

- 3x Peristaltic pumps
- 2x 12v self-priming pump
- 12-pin panel-mounted female Phoenix-style connector
  - 3x the half of the stepper motor cables that connect to the stepper motors themselves
- 8-pin panel-mounted female Phoenix-style connector
- 2x Female barrel plug connector (5.5mm x 2.1mm)
- TODO: Maybe some wire connectors in here as well
- 20x 16mm M3 screws
- 4x 30mm M3 screws

### Printed Parts

- Pumps Unit box
- Pumps Unit lid

## Assembling the Pumps Unit

### Mounting the Components to the Box

First, we're going to mount the pumps to the front of the box and install the plugs for the stirring motor and light.

<IMG ALT="Pump unit box and parts" SRC="./media/pumps-unit/pumps-unit-box-parts.jpg" WIDTH="400" />
<IMG ALT="Pump unit box and parts" SRC="./media/pumps-unit/pumps-unit-box-assembled.jpg" WIDTH="400" />

**Components:**

- Pumps Unit box
- 3x Peristaltic pumps
- 2x 12v self-priming pump
- 20x 16mm M3 screws
- 2x Female barrel plug connector (5.5mm x 2.1mm)
- TODO: Maybe some wire connectors in here as well

**Assembly:**

- Screw or press the 2x female barrel plug connectors into the holes on the front of the box. Secure them with any included nuts.
  - NOTE: Because the bottom hole is so close to the edge, you may need to use pliers to screw the barrel plug socket into the nut rather than screwing the nut onto the connector.
- Place each of the peristaltic pumps in one of the large holes and screw them in with the M3 screws and nuts.
- Attach the 12v self-priming circulation pumps to the inside of the box using the manufacturer-provided mounting hardware and M3 screws.
  - Many pumps come with rubber mounts that fit the two screw holes on the front of the box. If your pump's mounting hardware is different, you may need to drill your own holes. If your pump does not come with mounting hardware, you may need to get creative. In a pinch, zipties should work although you may want to double them up or drill out the holes to support thicker ties.
  - NOTE: [We are looking into better solutions for this and suggestions are welcome](https://github.com/FourThievesVinegar/solderless-microlab/issues/184).

## Mounting and Wiring the Lid

Next, we'll install the Phoenix connector sockets and wire them to the components we just installed. If you have already built the Control Unit, you will now see how the connections you made earlier connect to the actual devices they will control.

<IMG ALT="Pump unit lid and parts" SRC="./media/pumps-unit/pumps-unit-lid-parts.jpg" WIDTH="400" />
<IMG ALT="Pump unit lid fully assembled" SRC="./media/pumps-unit/pumps-unit-lid-assembled.jpg" WIDTH="400" />
<IMG ALT="Pump unit fully assembled with the lid open and wire connections visible" SRC="./media/pumps-unit/pumps-unit-lid-open.jpg" WIDTH="400" />

**Components:**

- Pumps Unit lid
- 12-pin panel-mounted female Phoenix-style connector
  - 3x the half of the stepper motor cables that connect to the stepper motors themselves
- 8-pin panel-mounted female Phoenix-style connector
- Additional wire connectors (as needed)

**Assembly:**

- Connect the Phoenix sockets with their mounting panels and use the M3 screws to attach them securely to the lid.
- Cut and strip the wires on the pumps and barrel plug connectors, then take a moment to plan your wiring.
  - The wiring here needs to reflect the wiring on the Control Unit. Imagine your ribbon cable running from one to the other (or plug it in and follow the connections!)
  - If you have made your cable as recommended in the Control Unit assembly instructions, you should be able to wire this 8-pin socket the same way you did on the Control Unit.
  - You may need wire connectors to extend the barrel plug leads.

```ascii
8-pin socket as seen from the outside

-----------------
|-|+|-|+|-|+|-|+|
-----------------
  ^   ^   ^   ^
Heat  |  Stir |
    Cool    Light
```

- Connect the 12-wire Phoenix connector to the motor-ends of the stepper motor cables
  - Make sure this matches how you wired your other connectors and cables. If needed, you can plug in the cable and trace the wires from the Control Unit to the Pumps Unit
- Plug the cables into the stepper motors

## Closing it up

- Finally, use the 30mm M3 screws to close the box using the lid.
  - NOTE: You may want to test everything before closing the lid. You can always open it again, but each time it wears the plastic and makes the screws looser. You might counteract this by adding tiny amounts of soft-ish material to the hole (just like you can put a matchstick in an over-used out screw hole in a piece of wood), but ultimately we are hoping to transition to a more durable method of closing the case.
  - The point is: you might wanna test your connections before closing everything up!

✨ 💖 ✨

Congratulations! You did it. That wasn't so bad, was it?

(Sorry if it was. We're trying to be encouraging here, not snarky.)

# Microlab Linear Syringe Pump Assembly

**Note:** this component can be replaced with off-the-shelf peristaltic pumps, which require less assembly.

The syringe pump is made up of 8 parts that must be printed. The parts are labelled Linear Actuator with a part number.
https://www.youmagine.com/designs/syringe-pump

![Syringe pump](/docs/media/syringe_pump2.png)

## Syringe pumps parts

- Metal rods
- Nuts
- Syringe pumps - 3D printed from STL file
  - Syringe Plunger holder??
  - Motor base [Part 3D-1]
- Motors (TODO: Verify these)
  - BIQU A4988 Compatible StepStick Stepper Motor Diver Module with Heat Sink for 3D Printer Controller Ramps 1.4(Pack of 5pcs)
  - Twotrees Stepper Motor Nema 17 Motor 42BYGH 1.8 Degree Body 38MM 4-Lead Wirel .5A 42N.cm (60oz.in) with 1 m Cable for DIY CNC 3D Printer (Pack of 3)
- Tubing (3/8”?)
  - Tubing to syringe pumps into reaction chamber (peristaltic pumps will come with their own tubing)

## Syringe Pumps assembly

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

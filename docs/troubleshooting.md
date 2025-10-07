# MicroLab Troubleshooting

The MicroLab is essentially a Linux box with an Arduino and some relays. You can always connect a keyboard to the open USB slot, hit ctrl + alt + F6 and log in as `thief` pw: `vinegard`. From here, if you know your way around a POSIX/Linux/Unix terminal, you can poke around. Check out [os-services.txt](https://github.com/FourThievesVinegar/solderless-microlab/blob/main/docs/os-services.txt) for more about how the MicroLab interfaces with the operating system.

## I'm getting an error message when I start the MicroLab

Open the menu and go to the Status page. This should have a button that says 'Reload Hardware'. Tap it gently until the status changes to "idle".

## My stepper motors are being weird! Stepper Motor Calibration.

We will need:

- Raspberry Pi that is set up
- Arduino that is set up
- Peristaltic pumps with stepper motors
- Small phillips head screw driver

### Potentiometer tuning

- On the Arduino, each A4988 stepper motor driver board has a small potentiometer that looks like a small phillips head screw on the board.
- If your peristaltic pumps are acting strange (not turning, or moving erratically), you **DEFINITELY** want to tune the potentiometers. In a worst-case scenario, motors may be damaged by excess voltage.

<IMG ALT="Potentiometer" SRC="./media/control-unit/potentiometers-annotated.jpg" WIDTH="600" />

Note:
In the image above, the potentiometers are circled and their slightly-flat sides are pointed to the left. This is the "slightly-open" position.

**WARNING!** Failure to correctly tune the potentiometers can damage the motor controller and the motors themselves.

#### How to tune

You will **gently** turn the potentiometers on the motor control boards clockwise or counter-clockwise using a small phillips head screw driver. Be careful to stop once there is any resistance, do not to turn past the resistance.

- Turning them clockwise "closes" the voltage down
- Turning them counter-clockwise "opens" the voltage up

1. Attach the Arduino's stepper motor cables to the stepper motor on the peristaltic pump.
1. Double-check that everything is connected properly.
1. Start with the potentiometers in the "closed" position.
1. Connect the Arduino to the Pi.
1. Power on the Raspberry Pi, the Arduino shield and the pumps.
1. On the Raspberry Pi, the MicroLab software will load. Load the Test Recipe and choose the Reagent Pumps test. This test will allow you to make the pumps each dispense 10ml.
1. When the potentiometer is "closed" nothing should happen. Slowly turn the potentiometer counter-clockwise an eighth of a turn at a time to "open" them. Check if the stepper motors turn smoothly. If they do not move, "open" the potentiometer an eighth-turn and try again. If they move erratically, your voltage is likely too high and you need to "close" the potentiometer.

- You can tune the potentiometers at any time, but it is easiest during assembly when the Control Unit case is open.

### Stepper motor verification

**This is a more in-depth way to test the function of the stepper motors. If you have tuned the potentiometers as described above and the motors turn smoothly, you do not need to perform these steps.**

Check each peristaltic pump's motor. With the cables and power disconnected, you should be able to spin the shaft of the stepper motor with your fingers and feel almost no resistance.

Testing the motor. Take a short length of wire and jumper the top two pins (Pins 1 and 2) of the connector together.

If the motor is wired correctly you should now feel some resistance when you spin the shaft (you should be able to feel the “steps” in the stepper motor). Repeat this procedure with the bottom two pins (Pins 3 and 4).

If you do not feel any change in resistance, try jumpering other combinations of pins until you identify the two pairs. See Troubleshooting Stepper Motor if you continue to have issues.

## My circulation pumps don't have mounting brackets! - Pumps Box Assembly

- If your pump does not come with mounting hardware, you may need to get creative. In a pinch, zipties should work. You may want to double them up or drill out the holes to support thicker ties.

## My Reactor Core is failing somehow!

Make sure you are using the new GL-45 reactor core. The previous multi-part manifold was not chemically or thermally resistant.

### Optimizing Heat Exchange

We recommend having a heat reservoir and a cold reservoir. This can be as simple as a small counter-top deep fryer with operational temperatures below 188.2 °C / 370.8 °F (the boiling point of propylene glycol) and a cooler of ice (or a small chest freezer). We're currently testing these and if you've got ideas, please [reach out](https://fourthievesvinegar.org/contact/)!

## My touch screen is messed up! - Touch Screen Settings

### The screen doesn't work

The small touchscreen doesn't work at all. It shows all white or fails to light up at all.

**Issue:**
Touchscreen doesn't light up at all

**Solution:**
This indicates a hardware problem. It's likely the screen isn't getting power or is broken. If you have extra screens or microcomputers, try a different screen or another computer. If none of this resolves the issue, you may need to order a replacement or reach out to the manufacturer for help

### X or Y touch screen axis is reversed

**Issue:**
Your touch screen works, but not correctly. Tapping near two of the corners kinda works, but the other two corners seem reversed.

**Solution:**
There is a configuration file change that should fix this. Open the following file.

```bash
sudo nano /etc/X11/xorg.conf.d/99-calibration.conf
```

Look for a line like this one:

```bash
Option "SwapAxes" "1"
```

Try changing that `"1"` to a `"0"` and restarting the Pi.

```bash
sudo shutdown -r now
```

If that doesn't work, try searching for the manufacturer and model number of your screen with terms like "swapped axes".

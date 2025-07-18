# MicroLab Troubleshooting

Touchscreen for Raspberry Pi (CU-RPI). Make sure you get the proper drivers – different manufacturers may require different drivers. For the linked model, try these: link
https://www.dropbox.com/scl/fo/hawpkmswazw5h7lv2p8vq/AJa3CosqXNYN0Y3zPbmVNjM/Driver?rlkey=ev89s381ag053wue395hf4ueb&e=1&subfolder_nav_tracking=1&dl=0

## Stepper Motor Calibration

Before we continue with assembly, we should tune the potentiometers and test the stepper motor wiring.

We will need:

- Raspberry Pi that is set up
- Arduino that is set up
- Peristaltic pumps with stepper motors
- Small phillips head screw driver

### Potentiometer tuning

- On the Arduino, each A4988 stepper motor driver board has a small potentiometer that looks like a small phillips head screw on the board.
- You **DEFINITELY** want to tune the potentiometers. If you don't, the stepper motors will likely behave strangely and could be damaged by excess voltage.

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
1. On the Raspberry Pi, the MicroLab software will load, locate the Test Recipe and choose to manually run each of the peristaltic pumps. **More detail needed**<br>
1. Slowly turn the potentiometer counter-clockwise an eighth of a turn at a time to "open" them. Check if the stepper motors turn smoothly. If they do not move, "open" the potentiometer an eighth-turn and try again. If they move erratically, your voltage is likely too high and you "close" the potentiometer.
1. Once tuned, power off the motors and the Raspberry Pi. Remove the stepper motor cables from the stepper motors of the peristaltic pumps.

- You can tune the potentiometers later as well, but the lid on the Control Unit will need to be off.

### Stepper motor verification

**This is a more in-depth way to test the function of the stepper motors. If you have tuned the potentiometers as described above and the motors turn smoothly, you do not need to perform these steps.**

Check each peristaltic pump's motor. With the cables and power disconnected, you should be able to spin the shaft of the stepper motor with your fingers and feel almost no resistance.

Testing the motor. Take a short length of wire and jumper the top two pins (Pins 1 and 2) of the connector together.

If the motor is wired correctly you should now feel some resistance when you spin the shaft (you should be able to feel the “steps” in the stepper motor). Repeat this procedure with the bottom two pins (Pins 3 and 4).

If you do not feel any change in resistance, try jumpering other combinations of pins until you identify the two pairs. See Troubleshooting Stepper Motor if you continue to have issues.

## Pumps Box Assembly

- If your pump does not come with mounting hardware, you may need to get creative. In a pinch, zipties should work although you may want to double them up or drill out the holes to support thicker ties.
- NOTE: [Suggestions for better solutions are welcome](https://github.com/FourThievesVinegar/solderless-microlab/issues/184).

### Reactor Core

Please note that we are experimenting with sinking nuts into various components for more reliable and durable connections. This is why the screw holes on top of the manifold are hexagonal at the top. Doing this requires a soldering iron and a steady hand, as the nuts have to be kept flats in order to accept screws.

The new GL-45 reactor does not require as much assembly. We are still developing it, but it is recommended in place of the original v0.6.0 reactore core assembly.

### Optimizing Heat Exchange

We are looking into upcycling heat sinks from old computers but are still experimenting - please reach out if you have done this or have suggestions.

## Touch Screen Settings

### The screen doesn't work

The small touchscreen doesn't work at all. It shows all white or fails to light up at all.

**Issue:**
Touchscreen doesn't light up at all

**Solution:**
This indicates a hardware problem. It's likely the screen isn't getting power or is broken. If you have extra screens or microcomputers, try a different screen or another computer. If none of this resolves the issue, you may need to order a replacement or reach out to the manufacturer for help

**Issue:**
Touchscreen lights up but is all white

**Solution:**
This likely indicates that the drivers are not properly installed. Check the screen manufacturer's documentation and ensure that you're following their instructions for installation. Check to make sure that your microcomputer is compatible with the screen and the display drivers. If the HDMI port still sends video, this may indicate that the driver installation was not completed.

### X or Y touch axis is reversed

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

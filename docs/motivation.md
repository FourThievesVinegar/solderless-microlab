# Motivation

This document briefly describes the project and its purpose.

## Background

Our goal is to build an open-source DIY automated controlled lab reactor that
people can assemble with parts available online. We hope this will do for chemistry
what the 3D printer did for manufacturing: provide a DIY, hackable, low-cost method to design and produce certain needful things that otherwise would be out of reach.

Eventually, we hope this will allow people to make certain medicines at home. We also hope it will empower them to believe more deeply in their own bodily autonomy. This is in line with our mission to deliver a de facto "Right to Repair" for the human body as a way of providing *harm reduction for the living*.

## The Tool: a Controlled Lab Reactor

A commercial one looks like this:

![commercial lab reactor](media/commercial-lab-reactor.jpg)

But it costs thousands of dollars and is only available to labs for purchase.

Its reaction vessel looks like this:

![commercial reaction vessel](media/commercial-reaction-vessel.jpg)

The reaction happens in the inner chamber. Hot or cold liquid is pumped
through the outer jacket to control the temperature. Reagents are dispensed
through ports on top and there is a stirring rod in the center.

## Microlab

Our solution, the Microlab, uses two concentric mason jars that
screw into a 3D printed manifold with ports for reagents, a temperature probe, a
stirring rod, and thermal regulator fluid input / output.

![von hippel reactor](media/von-hippel-reactor.png)

A small mason jar screws into the bottom, while a larger mason jar screws into
the top.

The reagents are held in syringes and loaded into pumps powered by stepper motors.
The thermal regulator fluid is delivered by pumps controlled by a relay. We heat the liquid with tea
warmer coils or cool it with an ice water bucket.

The hardware is driven by a Raspberry Pi, which controls relays and stepper motors used to activate the Microlab's various features. The parts can be assembled without soldering.

The user selects "recipes" - reactions to run - from an integrated touch screen menu. The recipe guides them, step-by-step, through the reaction, controls the temperature, and automatically dispenses the correct amount of reagents at the right times.

## Being the Cyberpunk Dystopia We Want to See in the World

In our current situation, closed-source, opaque, unaccountable systems govern us from afar. We live our lives at the mercy of the state, the dollar, and the algorithm. These forces smile benevolently on some while they ignore or discipline others. With this project, we hope to nudge the world toward a future where each of us can help and heal one another and ourselves directly, without the need to supplicate to modern day gods and masters.
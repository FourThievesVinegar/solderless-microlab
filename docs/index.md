# Welcome to The Microlab

![Built Microlab](/docs/media/microlab-on-bench-labeled.jpg)

## Meet the Microlab Suite
|||
|-----|-----|
|![Microlab](media/microlab_logo.png)|**The Microlab** - A DIY automated lab that you download, 3D print, and assemble with commonly available hardware. The MicroLab works together with a suite of apps to guide and automate a variety of lifesaving drugs from your home.|
| ![Vinni](media/vinni_logo.png) | **Vinni** - Your guide to your new medical laboratory. Vinni keeps track of your projects including "recipes" from the Apocatherium and compounds of interest from Chemhacktica. Stay tuned for updates on Vinni's ability to help you sift through all the latest scientific literature. |
| ![Apothecarium](media/apoth_logo.png) | **Apothecarium** - A simple interface to create "recipes" - sets of instructions the Microlab uses to run chemical reactions. |
| ![Chemhacktica](media/chem_logo.png) | **Chemhacktica** - A tool that uses machine learning to automagically discover reaction pathways to target compounds. |

## What is the Microlab?

The Microlab is a do-it-yourself Controlled Lab Reactor. (CLR)  You don’t need a CLR to make chemical reactions happen, but it makes the process of synthesizing compounds from precursors much easier and more reliable. 
 
A CLR is to organic chemistry what an espresso machine is to coffee. It is possible to make coffee over an open fire with nothing more than beans, water, and a tin can. But you will get a better, more consistent cup of coffee from an automatic machine that dispenses the right amount of water at the right temperature in such a way that ensures the water is in contact with the grounds for the right amount of time.

Commercial CLRs are the equivalent of high end, fully automatic espresso machines. As long as the appropriate reservoirs are filled with beans, water, milk, and flavoring, anyone can craft a perfect mocha topped with steamed milk at the touch of a button.
 
The Microlab is more like a home espresso machine that will let you reliably make a good cappuccino but won’t do every single step for you. For both the espresso machine and the CLR you need to understand basic lab procedures, measurement techniques, and safety.
 
The Microlab is designed to load a recipe for a chemical reaction, then automate the temperature control, reagent addition, and stirring that are needed. It is designed for small-molecule organic chemistry to make certain medicinal compounds in your own home or workshop. 
  
### How does a Controlled Lab Reactor (CLR) work?

A CLR has 3 main jobs.

1. Maintain the ideal reaction conditions

    The core of a CLR is a temperature controlled vessel (the smaller mason jar) where the chemical reaction takes place. The reaction vessel is surrounded by an outer vessel (the large mason jar) through which hot or cold water is continuously circulated to keep the reaction at the correct temperature. Advanced CLRs often have mechanisms for regulating pressure, pH, and otherwise maintaining ideal conditions for the desired reaction to take place.

1. Mix the reactants

    The microlab achieves this with a stirring rod driven by a small motor that is switched on and off by a relay. Commercial systems may have significantly more powerful mixing systems with a variety of paddles that can handle large quantities of liquids with varying viscosity, but they function in the same way.

1. Allow materials to be added and removed from the reaction vessel

    CLRs need a way to introduce precise quantities of reactants into the reaction vessel without disturbing the reaction conditions. This can be as simple as a graduated cylinder with a stopcock, or in the case of the microlab, a set of computer controlled syringes. The microlab software dispenses the correct quantities at the correct time, reducing the chance of user error. Commercial CLRs also have a way to drain the reaction vessel without disassembling the reactor, but the microlab lacks this feature.
 
## Microlab Overview
The Microlab is made up of a Reactor Unit, Reagent Pump Unit, Temperature Control Unit, and Lab Control Unit. Once built, the Microlab can be set up with the appropriate chemicals and use a recipe file created in the Apothecarium software to automatically run chemical reactions. 

## Further Documentation

    docs/
        index.md      # The documentation homepage  (you are here)
        assembly.md   # How to build the microlab
        operation.md  # How to use it (currently a stub)
        

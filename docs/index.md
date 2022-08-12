# Welcome to Microlab
&nbsp;





## Meet the Microlab Suite

![Microlab](media/microlab_logo.png){ align=left style="height:10%;width:10%"} 
&nbsp;

**The Microlab** - a DIY automated lab that you download, 3D print and assemble with commonly available hardware. The MicroLab works together with a suite of apps to guide and automate a variety of lifesaving drugs from your home.</p>
&nbsp;


![Vinni](media/vinni_logo.png){ align=left style="height:10%;width:10%"} 
&nbsp;

**Vinni** - walks you through to your new medical laboratory. If this is the first time you’re using the MicroLab, we recommend having a chat with Vinni before using the Apocatherium and Chemhacktica.</p>
 &nbsp;

![Apothecarium](media/apoth_logo.png){ align=left style="height:10%;width:10%"} 
&nbsp;


**Apothecarium** - A book of recipes to make your own drugs. It provides step-by-step walk-throughs for you to use the MicroLab for drug synthesis.</p>
 &nbsp;

&nbsp;![Chemhacktica](media/chem_logo.png){ align=left style="height:10%;width:10%"} 
&nbsp;

**Chemhacktica** - Developer code that integrates with the suite of tools. Chemhacktica uses machine learning to automagically discover reaction pathways to target compounds.
 &nbsp;</p>

 
 &nbsp;
&nbsp;

![Microlab](media/microlab_logo.png){ align=left style="height:10%;width:10%"} 
&nbsp;

## What is Microlab?
</p>
&nbsp;

The Microlab is a do-it-yourself Controlled Lab Reactor. (CLR)  You don’t need a CLR to make chemical reactions happen, but it makes the process of synthesizing compounds from precursors much easier and more reliable. 
 
A CLR is to organic chemistry what an espresso machine is to coffee. It is possible to make coffee over an open fire with nothing more than beans, water, and a tin can. But, you will get a better, and more consistent cup of coffee from an automatic machine that dispenses the right amount of water at the right temperature in such a way that ensures the water is in contact with the grounds for the right amount of time.

Commercial CLRs are the equivalent of high end, fully automatic espresso machines. As long as the appropriate reservoirs are filled with beans, water, milk, and flavoring, anyone can craft a perfect mocha topped with steamed milk at the touch of a button.
 
The Microlab is more like a home espresso machine that will let you reliably make a good cappuccino but won’t do every single step for you. For both the espresso machine and the CLR you need to understand basic lab procedures, measurement techniques, and safety.
 
The Microlab is designed to load a recipe for a chemical reaction, and automate the temperature control, ingredient addition, and stirring that are needed for many simple reactions.  This can be used as an important step in making medicinal compounds in your own home or workshop. 
 
This document is a set of instructions for building one for yourself or members of your community. 
 
 
 
### How does a Controlled Lab Reactor (CLR) work?

A CLR has 3 main jobs.

1. Maintain the ideal reaction conditions

    The core of a CLR is a temperature controlled vessel (the smaller mason jar) where the chemical reaction takes place. The reaction vessel is surrounded by an outer vessel (the large mason jar) through which hot or cold water is continuously circulated to keep the reaction at the correct temperature. Advanced CLRs often have mechanisms for regulating pressure, pH, and otherwise maintaining ideal conditions for the desired reaction to take place.

1. Mix the reactants

    The microlab achieves this with a stirring rod driven by a small motor that is switched on and off by a relay. Commercial systems may have significantly more powerful mixing systems with a variety of paddles that can handle large quantities of liquids with varying viscosity, but they function in the same way.

1. Allow materials to be added and removed from the reaction vessel

    CLRs need a way to introduce precise quantities of reactants into the reaction vessel without disturbing the reaction conditions. This can be as simple as a graduated cylinder with a stopcock, or in the case of the microlab, a pair of computer controlled syringes. The microlab software dispenses the correct quantities at the correct time, reducing the chance of user error. Commercial CLRs also have a way to drain the reaction vessel without disassembling the reactor, but the microlab lacks this feature.
 
## Microlab Overview
The Microlab is made up of a reaction chamber, syringe pumps and control boards. Once built the Microlab can be set up with the appropriate chemicals and use a formula to mix the correct dose. 

This project is focused on the building and using of the Microlab. 


## Project layout

    mkdocs.yml        # The configuration file.
    docs/
        index.md      # The documentation homepage.
        assembly.md   # How to build the microlab
        operation.md  # How to use it

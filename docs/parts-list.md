# MicroLab Parts List

NOTE 1: We link to places that have the parts that we used. They aren't picked for best price or universal availability
NOTE 2: Saving money - check the price of a part in multiples, it may be cheaper than buying just one

## CONTROL UNIT (CU)

|  Part ID	| Count	| Name	        | Primary Link    |	Secondary Link |	Description / Notes |
| --------  | --    | ------------- |  -------------  | -------------- | -------------- |
| CU-RPI	  | 1	    |Raspberry Pi 3 Model B Board |	[Amazon link](https://www.amazon.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/dp/B07BDR5PDW)	| [Amazon Le Potato link 2](https://www.amazon.com/gp/product/B0BQG668P6)|	Primary link is to a Raspberry 3b+'s which is the most extensively tested.   Second link is for devlopers, we have experimental support for Le Potato by Libre Computer (link2). |
| CU-SCR	    | 1	    |Touchscreen for Raspberry Pi	| [Amazon link](https://www.amazon.com/dp/B0DQD3RFCT)|  |		Touchscreen for Raspberry Pi (CU-RPI).  Minimum recommended screen resolution is 640 x 480. |
| CU-SD32	| 1	| Micro SD card, 32GB |	[Amazon link](https://www.amazon.com/SanDisk-Extreme-microSDHC-Memory-Adapter/dp/B06XYHN68L/)| |		32GB is the minimum. If you make a new image on a larger card, you can use Pi Shrink to remove empty space from the disk image. If you shrink to the minimum, you may need to re-expand or your partition will run out of space|
| CU-UPC	| 1	 | Micro USB Cable, right angle |	[Amazon Link](https://www.amazon.com/Durable-Braided-Android-Charging-Samsung/dp/B09XK4JDBJ) |	|	Power cable for Raspberry Pi (CU-RPI). The right angle (90 degree) connector will fit better in the Control Unit case. You will need a cable that fits your Pi, we linked to a Micro USB (although newer board usually use USB C). |
| CU-UNO	| 1	| Arduino UNO	| [Amazon link (kit)](https://www.amazon.com/DAOKI-Expansion-Arduino-Heatsink-Engraving/dp/B08KFYKKN4) - be sure to pick option with UNO board	| [Amazon link](https://smile.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/) |	Links to kit will include Uno, CNC shield, motor drivers modules andle USB A/B cable. |
| CU-CNC	| 1 | 	Arduino CNC shield	| Included in kit	| | |	
| CU-SMD |	3	| Stepper Motor Drivers [For CU-CNC]		| Included in kit | | |
| CU-A2B	| 1	| USB A/B cable for Raspberry Pi to Arduino | Included in kit | | |			
| CU-RLY |	1 |	4-Channel Relay Board	 | [Amazon link](https://www.amazon.com/gp/product/B07BDJJTLZ/) | | |		
| CU-WCL	| 1	| Wire Connector (lever), 2-in-6-out	 | [Ali Express link](https://www.aliexpress.us/item/3256805430655743.html) | 	[Amazon link](https://www.amazon.com/gp/product/B08QMLSMC6) - assortment	| Called the 12V Wire Connector. The 2-in-6-out wire connector is used for 12V wiring. The 65-pack in the second link is enough to make multiple MicroLabs, smaller packs are avaiable but will be a higher cost per connector. This part is makes the wiring easier, but it can be replaced by any reliable method of splicing wires. |
| CU-JMP	| 5	| Breadboard Jumper Wires, male-female	| [Amazon link](https://www.amazon.com/Elegoo-EL-CP-004-Multicolored-Breadboard-arduino/dp/B01EV70C78) | |		Small wires to connect the pins on the Pi to other components.  |
| CU-POW	| 1	| Power Supply, 12V 5A	| [Amazon link](https://www.amazon.com/gp/product/B07GFFG1BQ)	| 	| This a 12v 5A power brick. If you’ve got one from an old laptop with a 5.5 x 2.1 mm plug, it may work just fine. Powers the MicroLab. |
| CU-CBC	| 1	| Control Case (Printed)	| Check the `/parts` directory	| [Github Link](https://github.com/FourThievesVinegar/microlab-parts/tree/master/v7/control-box)	| The docs index page goes into more detail about the 3D printed parts. |
| CU-CBL	| 1	| Control Lid (Printed)	| Check the `/parts` directory	| [Github Link](https://github.com/FourThievesVinegar/microlab-parts/tree/master/v7/control-box)	| The docs index page goes into more detail about the 3D printed parts. |
| CU-CCP	| 1	| Converter case (Printed)	| Check the `/parts` directory	| [Github Link](https://github.com/FourThievesVinegar/microlab-parts/tree/master/v7/control-box/sub-components) |	The docs index page goes into more detail about the 3D printed parts. 
| CU-RCP	| 1	| Relay case (Printed)	| Check the `/parts` directory	| [Github Link](https://github.com/FourThievesVinegar/microlab-parts/tree/master/v7/control-box/sub-components) |	The docs index page goes into more detail about the 3D printed parts. 
| CU-PLG  |	2	| Barrel plug connectors, 5.5mm x 2.1mm	| [Amazon link](https://www.amazon.com/gp/product/B08SJM2G52)| |		Connector with wires, 1 female and 1 male.|
| CU-USB	| 2	| Mountable USB cables	| [Ali Express Link](https://www.aliexpress.us/item/2261800163146375.html) |	[Amazon Link](https://www.amazon.com/Extension-Various-Chassis-Cabinets-Extender/dp/B09SQ86ZJM/?th=1)	| Straight connectors will work best, shorter length (25cm) is recommended. |
| CU-SDC	| 1	| 12V to 5V Converter, stepdown |	[Amazon link](https://www.amazon.com/gp/product/B07XXWQ49N) |	[Ali Express Link](https://www.aliexpress.us/item/3256805964676363.html)	|Stepdown converter with barrel connector and USB ports. |
|CU-RAH	| 1	| Right angle header row	| [Amazon link](https://www.amazon.com/Right-Female-Header-2-54mm-Connector/dp/B00R1M3JRQ)	|	
| CU-WCS |	1	| Wire Cutter and Stripper| 	[Amazon link](https://www.amazon.com/WGGE-Professional-crimping-Multi-Tool-Multi-Function/dp/B073YG65N2)	|	
| CU-FCT	| 1	| Flush cutters	| [Amazon link](https://www.amazon.com/Hakko-CHP-170-Micro-Cutter/dp/B00FZPDG1K)		
| CU-NNP	| 1	| Needle-nose pilers	| [Amazon link](https://www.amazon.com/Dykes-Needle-Pliers-Cutter-5-Inch/dp/B0733P4KZ5)	|	


## Shared Parts

|  Part ID	| Count	| Name	        | Primary Link    |	Secondary Link |	Description / Notes |
| --------  | --    | ------------- |  -------------  | -------------- | -------------- |
| SP-CAB	| 15ft roll |	4-wire cable, 18 gauge	| [Amazon link](https://www.amazon.com/gp/product/B07SJGHMX2)	|	| [Control Unit] [Pumps Box] 10 feet will be used to make cables to connect the Control Unit and the Pumps unit. Some of the rest will be used to wire components within the Control Unit. You can also use wires from ethernet cables.
| SP-RBW	| 40ft  roll	| 2-wire cable, red and Black , 18 gauge	| [Amazon link](https://www.amazon.com/TYUMEN-Electrical-Extension-Flexible-Lighting/dp/B01LZRV0HV)	|	| Optional and we won't use all of it, you may want to get a smaller amount if you can find it cheaper. Or just use ethernet cable.
| SP-SWW	| 15ft roll	| Split Wire Wrap, half-inch	| [Amazon link](https://www.amazon.com/AIRIC-10feet-Management-Retardant-Protector/dp/B0BFHT9XG8)		| | [Control Unit] [Pumps Box]
| SP-PC12	| 2	| 12-pin connector, panel-mount screw terminal | 	[Ali Express  link](https://www.aliexpress.us/item/3256805663080411.html)	|	|[Control Unit] [Pumps Box]  connector has three pieces: plug, mount plate and socket
|SP-PC8	| 2	| 8-pin connector, panel-mount screw terminal 	|||		[Control Unit] [Pumps Box] connector has three pieces: plug, mount plate and socket
| SP-PC2	| 1	| 2-pin connector, panel-mount screw terminal |	|	|	[Control Unit] connector has three pieces: plug, mount plate and socket
| SP-M3S-12	| 23	| 12mm M3 screws with nuts (Optional)| 	[Amazon link](https://www.amazon.com/gp/product/B09WMCWPRL/) - assortment	| |	[Reactor Unit] 20 for reactor stand (Optional, for the screw-together version)
| SP-M3S-16	| 28	| 16mm M3 screws with nuts	|||		[Control Unit] [Pumps]  20 for Pumps Box, 8 Control Unit
| SP-M3S-20	| 2	| 20mm M3 screws with nuts	|	|	| [Control Unit] [Reactor]  2 for Control Unit
| SP-M3S-30	| 5	| 30mm | M3 screws with nuts	|	|	Pumps Box 4
| SP-SMC	| 6	| Stepper motor cables	| included w/ peristaltic pumps	|	|The 3 stepper motors come with their own cable, but will need to cut  in half and both ends stripped. The linked ones are ready to use. 
| SP-ETN	| 1 roll	| Electrical tape, narrow	| [Amazon link](https://www.amazon.com/Ancor-Marine-Products-Electrical-Assorted/dp/B01CZ30AY0)	|	| 1" is most common, 1/2" should be narrow enough

## TEMPERATURE CONTROL UNIT

|  Part ID	| Count	| Name	        | Primary Link    |	Secondary Link |	Description / Notes |
| --------  | --    | ------------- |  -------------  | -------------- | -------------- |
| TC-PMP	| 2	| Circulating pump	| [Amazon link](https://www.amazon.com/dp/B09XH1GYYQ)	||	To run both heating and cooling in the same recipe without hardware reconfiguration between recipe steps, 2 pumps are required.  NOTE: Operational limits to pumps in terms of capacity and temperature have not been determined. Larger pumps may be desired for optimal operation, especially at high temperatures. Self-priming pumps are HIGHLY recommended.  NOTE: These will actually be installed in the Pumps Unit.
| TC-CTB	| 2	| Copper tubing 10’ ¼" OD x 3/16" ID	| [Amazon link for raw copper tubing](https://www.amazon.com/dp/B0B6RQ73JQ) |	[Amazon link](https://www.amazon.com/dp/B07FTQJXD7/) for aluminum cooler	| Copper tubing should fit snugly within the silicone tubing. This 10’ length should be enough to make 1 dense or 2 loose heat exchanger coils.   Pre-formed coils used for chilling in beer brewing are more expensive, but easier. These are also typically too large for even wide-mouth mason jars, so another container may be needed. We currently recommend using a countertop deep fryer or robust hot plate for a heat source
| TC-STB	| 1	| Silicone tubing 8mm OD x 5mm ID	| [Amazon link](https://www.amazon.com/dp/B08PTX867M)	|	| Silicone tubing should fit snugly around the copper tubing 
| TC-TAP |	1	| Tape for the insulation|			
| TC-TCT	| 1	| Copper tube cutter tool (optional) |	[Amazon link](https://www.amazon.com/tubing-cutter-brake-line-cutting/dp/B084ZV5BXP)| |	Only required for cutting copper tubing for experimenting with heat exchangers, which is not required.	
| TC-CTJ	| 1	| Copper tube jig	| | | Large dowel or round section of pipe ~5cm dimeter or larger is good       
| TC-LIQ	| 1	 | Liquid, propylene glycol, water, oil, or other	|		| | For temperature exchange with the Reactor Core. We have been using propylene glycol which support temperature ranges as high and as low as the MicroLab supports.

## REACTOR UNIT

|  Part ID	| Count	| Name	        | Primary Link    |	Secondary Link |	Description / Notes |
| --------  | --    | ------------- |  -------------  | -------------- | -------------- |
| RU-SRM	| 1	| Stir rod motor	| [Amazon link](https://www.amazon.com/gp/product/B07FVQ7VPX)	|	[Amazon link](https://www.amazon.com/gp/product/B09XB8TXJC) |  This link is to a 100 RPM 12v motor. You can also buy a faster motor and use a PWM controller to adjust the speed manually.
| RU-STR	| 1	| Stir rod | [Amazon link](https://www.amazon.com/gp/product/B07WRKQY7R)| |		Mixing paddle needs to be coated / PTFE. Stainless steel may react. Paddle should be small enough to fit easily in the 6oz mason jar
| RU-SRC |	1| 	Stir rod coupler | 4mm-to-5mm	| [Amazon link](https://www.amazon.com/dp/B0867R2N1R)		
| RU-PTFE	| 1	| PTFE Sheet	| [Amazon Link](https://www.amazon.com/dp/B094WBY9J6)	|	
| RU-RJF	| 2	| Jar Flanges (Printed)	| Check the `/parts` directory	|	[Github Link](https://github.com/FourThievesVinegar/microlab-parts/blob/master/v7/reactor-stand/reactor-stand-jar-flange.v0.1.STL)	|
| RU-COR	| 1	| 250ml GL45 Borosilicate Glass Bottles	|	[Amazon link](https://www.amazon.com/dp/B09JN683F9) | |	
| RU-OUT	| 1	| 32oz wide mouth mason jar for outer jacket	| [Amazon link](https://smile.amazon.com/Ball-Quart-Silver-Wide-Mouth/dp/B00G9DNO28/)		
| RU-SDH	| 1	| Reactor stand - H  (Printed)	| Check the `/parts` directory	|	Github Link |	H shaped piece for the reactor stand
| RU-SDA	| 1	| Reactor stand - A  (Printed)	| Check the `/parts` directory	|	Github Link	| A shaped piece for the reactor stand
| RU-SDC	| 1	| Reactor stand - ¢  (Printed)	| Check the `/parts` directory	|	Github Link |	¢ shaped piece for the reactor stand
| RU-SDK	| 1	| Reactor stand - K  (Printed)	| Check the `/parts` directory	|	Github Link |	K  shaped piece for the reactor stand
| RU-TMP	| 1	| Thermistor |	[Ali Express link](https://m.aliexpress.com/item/32827261401.html)	| |	Used to monitor the temperature in the reaction chamber. This is a link to a USB DS18B20 
| RU-PPM	| 3	| Peristaltic pumps with stepper motors	| [Amazon link](https://www.amazon.com/gp/product/B082K6CYV1)	| [Alibaba Link](https://www.alibaba.com/product-detail/Peristaltic-Pump-stepper-12V-DC-High_1600102647756.html)	| The 3 stepper motors should come with their own cable, but will need to cut in half and split between the Control Unit and the pumps box.  NOTE: Those links are likely to be sold out. There are other stepper-driven pumps, but they will not interface seamlessly with the printed parts. We’re also looking for DIY/printable designs.
| RU-SYR	| 3	| Syringes	| [Amazon link](https://www.calvetsupply.com/exel-syringe-without-needle-single-syringe-25-cc.html)	||	20 or 30mL are standard sizes. You may want more of these or different sizes.
| RU-PUB	| 1	| Pumps box (Printed)	| Check the `/parts` directory	|	[Github Link](https://github.com/FourThievesVinegar/microlab-parts/tree/master/v7/pumps-box) |	Case to put pumps and motors in 
| RU-PUL	| 1	| Pumps lid (Printed)	| Check the `/parts` directory	|	[Github Link](https://github.com/FourThievesVinegar/microlab-parts/tree/master/v7/pumps-box) |	Lid for pumps case
| RU-SUP	| 1	| Wire coat hanger|||			Used to support the syringes

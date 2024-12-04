from hardware.reagentdispenser.base import ReagentDispenser
import logging
import math


class SyringePump(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict, devices: dict):
        """
        Constructor. Initializes the pumps.
        :param reagent_dispenser_config:
          dict
            grblID
                string - device id for grbl
            syringePumpsConfig
                dict - Configuration for the syringe pump motors

                X
                    dict - configuration of the X axis/motor

                    mmPerRev
                        Number of mm the stepper motor moves per full revolution,
                        this is the pitch of the threaded rod
                    stepsPerRev
                        Number of steps per revolution of the stepper motor,
                        reference the documentation for the motor
                    mmPerml
                        Number of mm of movement needed to dispense 1 ml of fluid,
                        this is the length of the syringe divided by its fluid capacity
                    maxmmPerMin
                        Maximum speed the motor should run in mm/min
                Y
                    dict - configuration of the Y axis/motor,
                    same as documented above but for the Y axis

                    mmPerRev
                    stepsPerRev
                    mmPerml
                    maxmmPerMin
                Z
                    dict - configuration of the Z axis/motor,
                    same as documented above but for the Z axis

                    mmPerRev
                    stepsPerRev
                    mmPerml
                    maxmmPerMin
        """
        self.grbl = devices[reagent_dispenser_config["grblID"]]
        self.syringePumpsConfig = reagent_dispenser_config["syringePumpsConfig"]
        self.axisMinmmPerMin = {}
        for axis, syringeConfig in self.syringePumpsConfig.items():
            stepsPerMM = syringeConfig["stepsPerRev"] / syringeConfig["mmPerRev"]
            axisToCNCID = {
                "X": "0",
                "Y": "1",
                "Z": "2",
            }
            self.axisMinmmPerMin[axis] = math.ceil((30 / stepsPerMM) * 120)
            # configure steps/mm
            self.grbl.grblWrite(
                "$10{0}={1}".format(axisToCNCID[axis], stepsPerMM)
            )
            # configure max mm/min
            self.grbl.grblWrite(
                "$11{0}={1}".format(axisToCNCID[axis], syringeConfig["maxmmPerMin"]),
            )

    def dispense(self, pumpId, volume, duration=None):
        """
        Dispense reagent from a syringe

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number of ml to dispense
        :return:
            None
        """

        maxmmPerMin = self.syringePumpsConfig[pumpId]["maxmmPerMin"]
        mmPerml = self.syringePumpsConfig[pumpId]["mmPerml"]
        dispenseSpeed = maxmmPerMin
        if duration:
            dispenseSpeed = min((volume / duration) * 60 * mmPerml, dispenseSpeed)
        totalmm = volume * mmPerml
        command = "G91 G1 {0}{1} F{2}".format(pumpId, totalmm, dispenseSpeed)
        logging.debug("Dispensing with command '{}'".format(command))
        self.grbl.grblWrite(command)
        dispenseTime = abs(totalmm) / (dispenseSpeed / 60)

        logging.info(
            "Dispensing {}ml with motor speed of {}mm/min over {} seconds".format(
                volume, dispenseSpeed, dispenseTime
            )
        )
        return dispenseTime

    def getPumpSpeedLimits(self, pumpId):
        maxSpeed = (
            self.syringePumpsConfig[pumpId]["maxmmPerMin"]
            / self.syringePumpsConfig[pumpId]["mmPerml"]
            / 60
        )
        minSpeed = (
            self.axisMinmmPerMin[pumpId]
            / self.syringePumpsConfig[pumpId]["mmPerml"]
            / 60
        )
        return {"minSpeed": minSpeed, "maxSpeed": maxSpeed}

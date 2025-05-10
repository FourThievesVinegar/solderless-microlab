from hardware.reagentdispenser.base import ReagentDispenser
import math
from util.logger import MultiprocessingLogger
from localization import load_translation


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
        self._logger = MultiprocessingLogger.get_logger(__name__)
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

    def dispense(self, pumpId: str, volume: int, duration: int = None) -> float:
        """
        Dispense reagent from a syringe

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number of ml to dispense
        :return:
            duration of the dispensation in seconds
        """
        t = load_translation()

        maxmmPerMin = self.syringePumpsConfig[pumpId]["maxmmPerMin"]
        mmPerml = self.syringePumpsConfig[pumpId]["mmPerml"]
        dispenseSpeed = maxmmPerMin
        if duration:
            dispenseSpeed = min((volume / duration) * 60 * mmPerml, dispenseSpeed)
        totalmm = volume * mmPerml
        command = "G91 G1 {0}{1} F{2}".format(pumpId, totalmm, dispenseSpeed)
        self._logger.debug(t['dispensing-command'].format(command))
        self.grbl.grblWrite(command)
        dispenseTime = abs(totalmm) / (dispenseSpeed / 60)

        self._logger.info(
            t['dispensing-specific'].format(
                volume, dispenseSpeed, dispenseTime
            )
        )
        return dispenseTime

    def getPumpSpeedLimits(self, pumpId: str) -> dict:
        t = load_translation()

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

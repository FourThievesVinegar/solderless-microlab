from hardware.reagentdispenser.base import ReagentDispenser
from util.logger import MultiprocessingLogger
from localization import load_translation

class PeristalticPump(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict, devices: dict):
        """
        Constructor. Initializes the pumps.
        :param args:
          dict
            grblID
                string - device id for grbl
            peristalticPumpsConfig
                dict - Configuration for the peristaltic pump motors
                F   Flow rate
                X
                    mmPerml   Arbitrary scaling factor
                Y
                    mmPerml   Arbitrary scaling factor
                Z
                    mmPerml   Arbitrary scaling factor
        """
        self._logger = MultiprocessingLogger.get_logger(__name__)
        self.grbl = devices[reagent_dispenser_config["grblID"]]
        self.peristalticPumpsConfig = reagent_dispenser_config["peristalticPumpsConfig"]
        self.grbl.grblWrite("G91")

    def dispense(self, pumpId, volume, duration=None) -> float:
        """
        Dispense reagent from a peristaltic pump

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number of ml to dispense
        :return:
            None
        """
        t=load_translation()
        
        fValue = self.peristalticPumpsConfig["F"]
        mmPerml = self.peristalticPumpsConfig[pumpId]["mmPerml"]
        totalmm = volume * mmPerml

        dispenseSpeed = fValue
        if duration:
            dispenseSpeed = min((volume / duration) * 60 * mmPerml, dispenseSpeed)
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

    def getPumpSpeedLimits(self, pumpId) -> dict:
        mmPerSecond = 30 / 250
        return {
            "minSpeed": mmPerSecond / self.peristalticPumpsConfig[pumpId]["mmPerml"],
            "maxSpeed": self.peristalticPumpsConfig["F"]
            * self.peristalticPumpsConfig[pumpId]["mmPerml"]
            / 60,
        }

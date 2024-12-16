import serial
from hardware.reagentdispenser.base import ReagentDispenser
from util.logger import MultiprocessingLogger

class PeristalticPump(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict):
        """
        Constructor. Initializes the pumps.
        :param args:
          dict
            arduinoPort
                string - Serial device for communication with the Arduino
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

        self.peristalticPumpsConfig = reagent_dispenser_config["peristalticPumpsConfig"]
        self.grblSer = serial.Serial(reagent_dispenser_config["arduinoPort"], 115200, timeout=1)
        self.grblWrite(self.grblSer, "G91")

    def dispense(self, pumpId, volume, duration=None):
        """
        Dispense reagent from a peristaltic pump

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number of ml to dispense
        :return:
            None
        """
        fValue = self.peristalticPumpsConfig["F"]
        mmPerml = self.peristalticPumpsConfig[pumpId]["mmPerml"]
        totalmm = volume * mmPerml

        dispenseSpeed = fValue
        if duration:
            dispenseSpeed = min((volume / duration) * 60 * mmPerml, dispenseSpeed)
        command = "G91 G1 {0}{1} F{2}\n".format(pumpId, totalmm, dispenseSpeed)
        self._logger.debug("Dispensing with command '{}'".format(command))
        self.grblWrite(self.grblSer, command)

        dispenseTime = abs(totalmm) / (dispenseSpeed / 60)
        self._logger.info(
            "Dispensing {}ml with motor speed of {}mm/min over {} seconds".format(
                volume, dispenseSpeed, dispenseTime
            )
        )
        return dispenseTime

    def getPumpSpeedLimits(self, pumpId):
        mmPerSecond = 30 / 250
        return {
            "minSpeed": mmPerSecond / self.peristalticPumpsConfig[pumpId]["mmPerml"],
            "maxSpeed": self.peristalticPumpsConfig["F"]
            * self.peristalticPumpsConfig[pumpId]["mmPerml"]
            / 60,
        }

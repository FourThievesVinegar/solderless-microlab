import time
import config
import serial
from hardware.reagentdispenser.base import ReagentDispenser
import logging


def grblWrite(grblSer, command, retries=3):
    """
    Writes the given command to grbl.

    :param grblSer:
    Serial device to write the command to

    :param command:
    String of grbl command to execute

    :return:
    None
    """
    grblSer.reset_input_buffer()
    grblSer.write(bytes(command, "utf-8"))
    # Grbl will execute commands in serial as soon as the previous is completed.
    # No need to wait until previous commands are complete. Ok only signifies that it
    # parsed the command
    response = grblSer.read_until()
    if "error" in str(response):
        if retries > 0:
            grblWrite(grblSer, command, retries - 1)
        else:
            raise Exception(
                "grbl error: {0} for command: {1}".format(response, command)
            )


class PeristalticPump(ReagentDispenser):
    def __init__(self, args):
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
        self.peristalticPumpsConfig = args["peristalticPumpsConfig"]
        self.grblSer = serial.Serial(args["arduinoPort"], 115200, timeout=1)
        grblWrite(self.grblSer, "G91")

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
        logging.debug("Dispensing with command '{}'".format(command))
        grblWrite(self.grblSer, command)

        dispenseTime = abs(totalmm) / (dispenseSpeed / 60)
        logging.info(
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

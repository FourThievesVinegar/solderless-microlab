from hardware.grbl.base import GRBL
import serial
from util.logger import MultiprocessingLogger

class GRBLSerial(GRBL):
    def __init__(self, grbl_config: dict):
        """
        Constructor. Initializes the serial device.
        :param args:
          dict
            grblPort
                string - Serial device for communication with grbl
        """
        self._logger = MultiprocessingLogger.get_logger(__name__)

        self.grblSer = serial.Serial(grbl_config["grblPort"], 115200, timeout=1)

    def grblWrite(self, command: str, retries=3):
        self.grblSer.reset_input_buffer()
        self.grblSer.write(bytes("{}\n".format(command), "utf-8"))
        # Grbl will execute commands in serial as soon as the previous is completed.
        # No need to wait until previous commands are complete. Ok only signifies that it
        # parsed the command
        response = self.grblSer.read_until()
        if "error" in str(response):
            if retries > 0:
                self._logger.warning("grbl error: {0} for command: {1}, retrying"
                                .format(response, command))
                self.grblWrite(command, retries - 1)
            else:
                raise Exception(
                    "grbl error: {0} for command: {1}".format(response, command)
                )

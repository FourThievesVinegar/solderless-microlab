import serial

from hardware.grbl.base import GRBL
from localization import load_translation


class GRBLSerial(GRBL):
    def __init__(self, grbl_config: dict):
        """
        Constructor. Initializes the serial device.
        :param grbl_config:
          dict
            grblPort
                string - Serial device for communication with grbl
        """
        chip_name = grbl_config['id']
        super().__init__(chip_name)

        self.grblSer = serial.Serial(grbl_config['grblPort'], 115200, timeout=1)

    def grblWrite(self, command: str, retries: int = 3) -> None:
        """ :inheritdoc: """
        t = load_translation()

        self.grblSer.reset_input_buffer()
        self.grblSer.write(bytes('{}\n'.format(command), 'utf-8'))
        # Grbl will execute commands in serial as soon as the previous is completed.
        # No need to wait until previous commands are complete. Ok only signifies that it
        # parsed the command
        response = self.grblSer.read_until()
        if 'error' in str(response):
            if retries > 0:
                self._logger.warning(t['grbl-error-retrying'].format(response, command))
                self.grblWrite(command, retries - 1)
            else:
                raise ValueError(t['grlb-error'].format(response, command))

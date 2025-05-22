import serial

from hardware.grbl.base import GRBL


class GRBLSerial(GRBL):
    def __init__(self, grbl_config: dict):
        """
        Constructor. Initializes the serial device.
        :param grbl_config:
          dict
            grblPort
                string - Serial device for communication with grbl
        """
        super().__init__(grbl_config['id'])
        self.device = serial.Serial(grbl_config['grblPort'], 115200, timeout=1)

    def grblWrite(self, command: str, retries: int = 3) -> None:
        """ :inheritdoc: """
        self.device.reset_input_buffer()
        self.device.write(bytes('{}\n'.format(command), 'utf-8'))

        # Grbl will execute commands in serial as soon as the previous is completed.
        # No need to wait until previous commands are complete. Ok only signifies that it
        # parsed the command
        response = self.device.read_until()
        if 'error' in str(response):
            if retries > 0:
                self._logger.warning(self.t['grbl-error-retrying'].format(response, command))
                self.grblWrite(command, retries - 1)
            else:
                raise ValueError(self.t['grlb-error'].format(response, command))

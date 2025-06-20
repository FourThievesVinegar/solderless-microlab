from abc import abstractmethod

from hardware.lab_device import LabDevice
from localization import load_translation


class GRBL(LabDevice):
    def __init__(self, device_name: str):
        super().__init__(device_name)
        self.t = load_translation()

    @abstractmethod
    def write_gcode(self, command: str, retries: int = 3) -> None:
        """
        Writes the gcode command to grbl

        :param command:
            The raw gcode command string.
        :param retries:
            Number of times to retry the command should it fail.
            default is 3
        :return:
            None
        """
        pass

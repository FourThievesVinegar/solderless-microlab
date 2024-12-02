from abc import ABC, abstractmethod

class GRBL:

    @abstractmethod
    def grblWrite(self, command: str, retries=3):
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

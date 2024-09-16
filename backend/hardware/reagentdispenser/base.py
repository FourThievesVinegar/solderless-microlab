from abc import ABC, abstractmethod


class ReagentDispenser(ABC):
    @abstractmethod
    def dispense(pumpId, volume, duration=None):
        """
        Dispense reagent.

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number ml to dispense
        :param duration:
            optional - How long the dispense should take in seconds
        :return:
            Number indicating how long the dispense should take to complete
        """
        pass

    @abstractmethod
    def getPumpSpeedLimits(pumpId):
        """
        Get maximum and minimum speed of specified pump.

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :return:
            dict
                minSpeed
                    Minimum speed the pump can dispense in ml/s
                maxSpeed
                    Maximum speed the pump can dispense in ml/s
        """
        pass

    @classmethod
    def grblWrite(cls, grblSer, command, retries=3):
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
                cls.grblWrite(grblSer, command, retries - 1)
            else:
                raise Exception(
                    "grbl error: {0} for command: {1}".format(response, command)
                )

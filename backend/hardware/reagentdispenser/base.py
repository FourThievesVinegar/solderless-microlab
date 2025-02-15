from abc import ABC, abstractmethod


class ReagentDispenser(ABC):
    @abstractmethod
    def dispense(self, pumpId, volume, duration=None):
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
    def getPumpSpeedLimits(self, pumpId):
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

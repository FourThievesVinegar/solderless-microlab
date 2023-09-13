from abc import ABC,abstractmethod

class ReagentDispenser(ABC):
    @abstractmethod
    def dispense(pumpId, volume):
        """
        Dispense reagent.

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number ml to dispense
        :return:
            None
        """
        pass

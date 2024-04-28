from abc import ABC,abstractmethod

LINE_REQ_DIR_OUT = 'output'
LINE_REQ_DIR_IN = 'input'

class GPIOChip(ABC):
    @abstractmethod
    def setup(self, pin, pinType, outputValue):
        """
        Sets up pin for use, currently only output is supported.

        :param pin:
            The pin to setup. Either a defined alias or the line number for the pin
        :param pinType:
            One of "output" or "input". Currently only "output" is supported
        :param outputValue:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        pass

    @abstractmethod
    def output(self, pin, value):
        """
        Outputs a new value to specified pin

        :param pin:
            The pin to output on. Either a defined alias or the line number for the pin
        :param outputValue:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        pass

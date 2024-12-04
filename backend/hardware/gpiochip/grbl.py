from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT
import logging

class GRBLChip(GPIOChip):
    def __init__(self, gpio_config: dict, devices: dict):
        """
        Constructor. Initializes the GPIO chip.
        :param gpio_config:
          dict
            grblID
              ID of the grbl device
            lineAliases
              dictionary mapping strings to pin numbers
              for adding human readable names to GPIO pins
        """
        self.grbl = devices[gpio_config["grblID"]]
        self.output_offsets = []
        self.output_values = []
        self.pinAliases = {}
        if 'lineAliases' in gpio_config:
            for alias, pin in gpio_config['lineAliases'].items():
                self.pinAliases[alias] = pin
        logging.debug(self.pinAliases)

    def __output(self):
        """
        Outputs values on every pin that has been setup
        """
        for (val, pin) in (zip(self.output_values, self.output_offsets)):
          if val == 0:
            command = "M65"
          else:
            command = "M64"

          self.grbl.grblWrite("{} P{}".format(command, pin))

    def __getPinNumber(self, pin: str | int):
        """
        Converts string aliases to the corresponding pin number
        Throws an exception if pin is an alias that does not exist.
        :param pin:
            The pin to get the pin number of.
        :return:
            The pin number for that pin
        """
        if isinstance(pin, str):
            if self.pinAliases[pin]:
                return self.pinAliases[pin]
            else:
                raise Exception("Invalid GPIO pin {0}".format(pin))
        else:
            return pin

    def setup(self, pin: str | int, pinType=LINE_REQ_DIR_OUT, outputValue=0):
        """
        Sets up pin for use, currently only output is supported.

        :param pin:
            The pin to setup. Either a defined alias or the pin number for the pin
        :param pinType:
            One of "output" or "input". Currently only "output" is supported
        :param outputValue:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        pinNumber = self.__getPinNumber(pin)
        
        if pinType == LINE_REQ_DIR_OUT:
            self.output_offsets.append(pinNumber)
            self.output_values.append(outputValue)
            self.__output()

    def output(self, pin: str | int, value: int):
        """
        Outputs a new value to specified pin

        :param pin:
            The pin to output on. Either a defined alias or the pin number for the pin
        :param outputValue:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        pinNumber = self.__getPinNumber(pin)
        index = self.output_offsets.index(pinNumber)
        self.output_values[index] = value
        self.__output()

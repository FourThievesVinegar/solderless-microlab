from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT
import logging


class GPIODChipset(GPIOChip):
    def __init__(self, gpio_config: dict, devices: dict):
        """
        Constructor. Initializes the GPIO chip.
        :param gpio_config:
          dict
            chipName
              Name of the chip according to gpiod
            lineAliases
              dictionary mapping strings to line numbers
              for adding human readable names to GPIO lines
        """
        self.chips = {
            "defaultChip": devices[gpio_config["defaultChipID"]],
        }
        for chipID in gpio_config['additionalChips']:
            self.chips[chipID] = devices[chipID]
        
        self.lineAliases = {}

        for chipID, chip in self.chips.items(): 
            for alias, line in chip.lineAliases.items():
                if alias in self.lineAliases:
                    logging.warning("GPIO line alias '{0}' has a conflict between chips {1} and {2}. Using {2}.".format(alias, chipID, self.lineAliases[alias]))
                    continue
            self.lineAliases[alias] = chipID
        logging.debug(self.lineAliases)

    def setup(self, pin, pinType=LINE_REQ_DIR_OUT, outputValue=0):
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
        chipID = self.lineAliases[pin]
        if chipID:
            return self.chips[chipID].setup(pin, pinType, outputValue)
        else:
            return self.chips["defaultChip"].setup(pin, pinType, outputValue)

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
        chipID = self.lineAliases[pin]
        if chipID:
            return self.chips[chipID].output(pin, value)
        else:
            return self.chips["defaultChip"].output(pin, value)

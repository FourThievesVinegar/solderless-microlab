from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT, LINE_REQ_DIR_IN
import gpiod

class GPIODChip(GPIOChip):
    def __init__(self, args):
        """
        Constructor. Initializes the GPIO chip.
        :param args:
          dict
            chipName
              Name of the chip according to gpiod
            lineAliases
              dictionary mapping strings to line numbers
              for adding human readable names to GPIO lines
        """
        self.output_offsets = []
        self.output_values = []
        self.output_lines = []
        self.chip = None
        self.lineAliases = {}
        self.chip = gpiod.Chip(args['chipName'])
        if 'lineAliases' in args:
          for alias, line in args['lineAliases'].items():
            self.lineAliases[alias] = line
        print(self.lineAliases)


    def __output(self):
        """
        Outputs values on every line that has been setup
        """
        lines = self.chip.get_lines(self.output_offsets)
        lines.request(consumer="microlab", type=gpiod.LINE_REQ_DIR_OUT)
        lines.set_values(self.output_values)
        lines.release()

    def __getLineNumber(self, pin):
        """
        Converts string aliases to the corresponding line number
        Throws an exception if pin is an alias that does not exist.
        :param pin:
            The pin to get the line number of.
        :return:
            The line number for that pin
        """
        if type(pin) == str:
          if self.lineAliases[pin]:
            return self.lineAliases[pin]
          else:
            raise Exception("Invalid GPIO pin {0}".format(pin))
        else:
          return pin

    def setup(self, pin, pinType=LINE_REQ_DIR_OUT, outputValue=0):
        """
        Sets up pin for use, currently only output is supported.

        :param pin:
            The pin to setup. Either a defined alias or the line number for the pin
        :param pinType:
            One of "output" or "input". Currently only "output is supported"
        :param outputValue:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        lineNumber = self.__getLineNumber(pin)
        
        if pinType == LINE_REQ_DIR_OUT:
          #line = self.chip.get_line(lineNumber)
          #line.request(consumer="microlab", type=gpiod.LINE_REQ_DIR_OUT)
          self.output_offsets.append(lineNumber)
          self.output_values.append(outputValue)
          #self.output_lines.append(line)
          self.__output()
        

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
        lineNumber = self.__getLineNumber(pin)
        index = self.output_offsets.index(lineNumber)
        self.output_values[index] = value
        self.__output()


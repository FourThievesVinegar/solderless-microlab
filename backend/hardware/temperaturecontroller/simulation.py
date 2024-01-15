import time
from hardware.temperaturecontroller.base import TempController

def log(message):
    print('tempcontroller.simulation - ' + str(message))


class SimulatedTempController(TempController):
    heating = False
    cooling = False
    temperature = 24
    def __init__(self, args):
        super().__init__(args, devices=None)
        self.maxTemp = args["maxTemp"]
        self.minTemp = args["minTemp"]

    def turnHeaterOn(self):
        """
        Sets the heater flag for the simulation.

        :return:
        None
        """
        log('Turning on heat')
        self.heating = True


    def turnHeaterOff(self):
        """
        Un-sets the heater flag for the simulation.

        :return:
        None
        """
        log('Turning off heat')
        self.heating = False


    def turnCoolerOn(self):
        """
        Sets the cooler flag for the simulation.

        :return:
        None
        """
        log('Turning on cooling')
        self.cooling = True


    def turnCoolerOff(self):
        """
        Un-sets the cooler flag for the simulation.

        :return:
        None
        """
        log('Turning off cooling')
        self.cooling = False


    def getTemp(self):
        """
        Simulates and returns temperature.

        Temperature starts off at 24C and changes every time the function is called as follows:
            heater flag on: +1C
            cooler flag on: -1C
            cooler and heater flag off: -0.1C
        :return:
        """
        if self.temperature == -1:
            self.temperature = 24
        else:
            if self.heating == True:
                self.temperature = self.temperature + 1
            elif self.cooling == True:
                self.temperature = self.temperature - 1
            else:
                if self.temperature > 24:
                    self.temperature = self.temperature - 0.1
                elif self.temperature < 24:
                    self.temperature = self.temperature + 0.1
        print('Temperature read as: {0}'.format(self.temperature))
        return self.temperature

    def getMaxTemperature(self):
        return self.maxTemp

    def getMinTemperature(self):
        return self.minTemp

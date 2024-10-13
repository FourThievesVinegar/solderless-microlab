from hardware.temperaturecontroller.base import TempController
import logging
import sys


def log(message):
    logging.info('tempcontroller.simulation - ' + str(message))


class SimulatedTempController(TempController):
    def __init__(self, sim_temp_controller_config: dict):
        super().__init__(sim_temp_controller_config, devices=None)
        self.maxTemp = sim_temp_controller_config["maxTemp"]
        self.minTemp = sim_temp_controller_config["minTemp"]
        self.heating = False
        self.cooling = False
        self.temperature = 24
        if 'temp' in sim_temp_controller_config:
            self.temperature = sim_temp_controller_config['temp']

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
        sys.stdout.write('Turning off heat in SimulatedTempController\n')
        sys.stdout.flush()
        self.heating = False

    def turnHeaterPumpOn(self):
        log("heater pump turned on")

    def turnHeaterPumpOff(self):
        log("heater pump turned off")
        sys.stdout.write('Turning off heater pump in SimulatedTempController\n')
        sys.stdout.flush()

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
        sys.stdout.write('Turning off cooling in SimulatedTempController\n')
        sys.stdout.flush()
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
            if self.heating is True:
                self.temperature = self.temperature + 1
            elif self.cooling is True:
                self.temperature = self.temperature - 1
            else:
                if self.temperature > 24:
                    self.temperature = self.temperature - 0.1
                elif self.temperature < 24:
                    self.temperature = self.temperature + 0.1
        logging.info('Temperature read as: {0}'.format(self.temperature))
        return self.temperature

    def getMaxTemperature(self):
        return self.maxTemp

    def getMinTemperature(self):
        return self.minTemp

    def getPIDConfig(self):
        """
        Read the temperature controller PID configuration

        :return:
        None if not specified, otherwise:
        object
            P: number
            I: number
            D: number
            proportionalOnMeasurement: Boolean (optional)
            differentialOnMeasurement: Boolean (optional)
        """
        return self.pidConfig

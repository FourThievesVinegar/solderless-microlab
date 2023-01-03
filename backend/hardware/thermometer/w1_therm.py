from hardware.thermometer.base import TempSensor
from w1thermsensor import W1ThermSensor, Sensor

class W1TempSensor(TempSensor):
    sensor = None
    def __init__(self):
        """
        Constructor. Saves the plan.
        :param plan:
        The recipe plan. See module documentation for object description.
        """
        self.sensor = W1ThermSensor()

    def getTemp(self):
        return self.sensor.get_temperature()

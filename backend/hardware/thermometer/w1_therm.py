from hardware.thermometer.base import TempSensor
from w1thermsensor import W1ThermSensor, Sensor

class W1TempSensor(TempSensor):
    sensor = None
    def __init__(self):
        """
        Constructor. Initializes the sensor.
        """
        self.sensor = W1ThermSensor()

    def getTemp(self):
        """
        Get the temperature of the sensor in celsius.
        :return:
            Temperature in Celsius
        """
        return self.sensor.get_temperature()

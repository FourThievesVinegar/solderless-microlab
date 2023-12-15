from hardware.thermometer.base import TempSensor
from w1thermsensor import W1ThermSensor, Sensor, SensorNotReadyError

class W1TempSensor(TempSensor):
    sensor = None
    lastTemp = 0
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
        try:
            self.lastTemp = self.sensor.get_temperature()
        except SensorNotReadyError:
            pass
        return self.lastTemp

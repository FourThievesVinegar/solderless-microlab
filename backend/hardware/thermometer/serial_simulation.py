from typing import Optional

from hardware.thermometer.base import TempSensor


class SerialTempSensorSimulation(TempSensor):
    def __init__(self, thermometer_config: dict):
        """
        Constructor. Initializes the sensor.
        :param thermometer_config:
          dict
            serialDevice
              A string with the device read from
        """
        super().__init__(thermometer_config['id'])
        self.temp: Optional[float] = thermometer_config.get('temp')

    def get_temp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        Recommended sensor: DS18B20

        A successful read looks something like this: b"t1=+29.06\n"
        The loop below looks for the '=' '\n' '.' to detect success

        :return:
            Temperature in Celsius
        """
        reading = self.temp if self.temp is not None else +29.06
        return float(reading)

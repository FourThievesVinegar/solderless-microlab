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
        self.tempSer = 0
        if 'temp' in thermometer_config:
            self.temp = thermometer_config['temp']

    def getTemp(self) -> float:
        """
        Get the temperature of the sensor in celsius.
        Recommended sensor: DS18B20

        A successful read looks something like this: b"t1=+29.06\n"
        The loop below looks for the '=' '\n' '.' to detect success

        :return:
            Temperature in Celsius
        """
        if self.temp:
            return self.temp
        line = "12345678901"
        lastLine = "+29.06"

        # Commenting the below line out for the time being, no 'start' or 'end' variables are defined so this will throw
        # an exception. Replacing it with just returning a float cast of 'lastLine' as that looks like a valid value
        # temperature = float(lastLine[start:end])

        temperature = float(lastLine[1:])  # Trimming off the '+' before casting
        return temperature

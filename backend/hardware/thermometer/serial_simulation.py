from hardware.thermometer.base import TempSensor
import time

class SerialTempSensorSimulation(TempSensor):
    def __init__(self, args):
        """
        Constructor. Initializes the sensor.
        :param args:
          dict
            serialDevice
              A string with the device read from
        """
        self.tempSer = 0
        if 'temp' in args:
          self.temp = args['temp']

    def getTemp(self):
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
        temperature = float(lastLine[start:end])
        return temperature
       
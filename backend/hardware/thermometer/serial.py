from hardware.thermometer.base import TempSensor
from w1thermsensor import W1ThermSensor, Sensor
import serial

class SerialTempSensor(TempSensor):
    tempSer = None
    def __init__(self, args):
        """
        Constructor. Initializes the sensor.
        :param args:
          dict
            serialDevice
              A string with the device read from
        """
        self.tempSer = serial.Serial(args["serialDevice"], timeout=0.5)

    def getTemp(self):
        """
        Get the temperature of the sensor in celsius.
        :return:
            Temperature in Celsius
        """
        line = "12345678901"
        lastLine = ""
        while (len(line) > 10):
            lastLine = line
            line = self.tempSer.readline()
            print('ser read ' + str(len(line)) + ' ' + str(line) )

        lastLine = str(lastLine)
        start = lastLine.find('t1=') + len('t1=')
        end = lastLine.find(' ',start)
        print('found ' + str(start) + ' ' + str(end) + ' ' + lastLine)
        temperature = float(lastLine[start:end])

        print('Read temperature ' + str(temperature)) # + ' ' + str(lastLine))
        return temperature

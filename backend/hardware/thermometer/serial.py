from hardware.thermometer.base import TempSensor
from w1thermsensor import W1ThermSensor, Sensor
import serial
import time
import logging

class SerialTempSensor(TempSensor):
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
        Recommended sensor: DS18B20

        A successful read looks something like this: b"t1=+29.06\n"
        The loop below looks for the '=' '\n' '.' to detect success

        :return:
            Temperature in Celsius
        """
        line = "12345678901"
        lastLine = ""
        while (line.find('\n') == -1 or line.find('=') == -1 or line.find('.') == -1):
            lastLine = line
            try:
                line = self.tempSer.readline().decode()
            except Exception as e:
                logging.error('Error reading from thermometer')
                logging.exception(str(e))
                continue
            finally:
                logging.debug('ser read ' + str(len(line)) + ' ' + line )
                time.sleep(0.1)

        lastLine = str(line)
   
        # Look for 't1=' or 't=' in the input line
        # Unclear why sometimes the thermometer returns 't1=' and other times just 't='
        # Use rfind because we want the last '=' and sometimes input includes extras
        start = lastLine.rfind('=') + len('=')

        end = lastLine.find('\\n',start)
        if end == -1:   # Different thermometers may parse differently. These conditionals may need to expand.
            end = lastLine.find(' ',start)
        if end == -1:   # Maybe just go to the end?
            end = len(lastLine) - 1
            
        logging.debug('found ' + str(start) + ' ' + str(end) + ' ' + lastLine + ' ' + lastLine[start:end]) 
        if(start > -1 and end > -1):
            try:
                temperature = float(lastLine[start:end])
            except Exception as e:
                logging.error('Error converting temperature reading')
                logging.error(lastLine[start:end])
                logging.exception(str(e))
                temperature = "Error"
        else:
            temperature = "Error"
        logging.debug('Read temperature ' + str(temperature)) # + ' ' + str(lastLine))

        return temperature

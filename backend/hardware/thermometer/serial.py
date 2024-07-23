from hardware.thermometer.base import TempSensor
import serial
import time
import logging
from hardware.util import HardwareLoadError
from datetime import datetime, timedelta


class SerialTempSensor(TempSensor):
    def __init__(self, args):
        """
        Constructor. Initializes the sensor.
        :param args:
          dict
            serialDevice
              A string with the device read from
        """
        self.lastTemp = 0
        self.nextTempReadingTime = datetime.now()

        try:
            self.tempSer = serial.Serial(args["serialDevice"], timeout=0.5)
        except serial.SerialException as e:
            raise HardwareLoadError(
                "Thermometer could not be detected at {}, make sure it's plugged in, try another USB port if it is, or change the device name in your lab hardware config file to the correct device name.".format(
                    args["serialDevice"]
                )
            ) from e

    def getTemp(self):
        """
        Get the temperature of the sensor in celsius.
        Recommended sensor: DS18B20

        A successful read looks something like this: b"t1=+29.06\n"
        It could also have single-digit temperatures
        The loop below looks for the '=' '\n' '.' to detect success

        :return:
            Temperature in Celsius
        """
        if datetime.now() > self.nextTempReadingTime:
            line = "12345678901"
            lastLine = ""
            while line.find("\n") == -1 or line.find("=") == -1 or line.find(".") == -1:
                lastLine = line
                try:
                    line = self.tempSer.readline().decode()
                except Exception as e:
                    logging.error("Error reading from thermometer")
                    logging.exception(str(e))
                    continue
                finally:
                    logging.debug("ser read " + str(len(line)) + " " + line)
                    time.sleep(0.5)

            lastLine = str(line)

            # Look for 't1=' or 't=' in the input line
            # Unclear why sometimes the thermometer returns 't1=' and other times just 't='
            # Use rfind because we want the last '=' and sometimes input includes extras
            start = lastLine.rfind("=") + len("=")

            end = lastLine.find("\\n", start)
            if (
                end == -1
            ):  # Different thermometers may parse differently. These conditionals may need to expand.
                end = lastLine.find(" ", start)
            if end == -1:  # Maybe just go to the end?
                end = len(lastLine) - 1

            logging.debug(
                "found "
                + str(start)
                + " "
                + str(end)
                + " "
                + lastLine
                + " "
                + lastLine[start:end]
            )
            # Make sure that we have a start and an end and that there is something between them
            if start > -1 and end > -1 and end - start > 2:
                try:
                    self.lastTemp = float(lastLine[start:end])
                except Exception as e:
                    logging.error("Error converting temperature reading")
                    logging.error(lastLine[start:end])
                    logging.exception(str(e))
                    temperature = "-999"
            else:
                temperature = "-999"
                logging.error("erroneous reading: {0}".format(lastLine[start:end]))
            logging.debug(
                "Read temperature " + str(temperature)
            )  # + ' ' + str(lastLine))

            self.nextTempReadingTime = datetime.now() + timedelta(seconds=1)

        return self.lastTemp

import time
from datetime import datetime, timedelta

import serial

from hardware.thermometer.base import TempSensor
from hardware.util.exceptions import HardwareLoadError
from localization import load_translation
from util.logger import MultiprocessingLogger


class SerialTempSensor(TempSensor):
    def __init__(self, thermometer_config: dict):
        """
        Constructor. Initializes the sensor.
        :param thermometer_config:
          dict
            serialDevice
              A string with the device read from
        """
        t = load_translation()

        self._logger = MultiprocessingLogger.get_logger(__name__)

        self.lastTemp = 0
        self.nextTempReadingTime = datetime.now()

        try:
            self.tempSer = serial.Serial(thermometer_config["serialDevice"], timeout=0.5)
        except serial.SerialException as e:
            raise HardwareLoadError(
                "Thermometer could not be detected at {}, make sure it's plugged in, try another USB port if it is, or change the device name in your lab hardware config file to the correct device name.".format(
                    thermometer_config["serialDevice"]
                )
            ) from e

    def getTemp(self) -> float:
        """
        Get the temperature of the sensor in celsius.
        Recommended sensor: DS18B20

        A successful read looks something like this: b"t1=+29.06\n"
        It could also have single-digit temperatures
        The loop below looks for the '=' '\n' '.' to detect success

        :return:
            Temperature in Celsius
        """
        t = load_translation()

        if datetime.now() < self.nextTempReadingTime:
            return self.lastTemp

        line = "12345678901"
        lastLine = ""
        while line.find("\n") == -1 or line.find("=") == -1 or line.find(".") == -1:
            lastLine = line
            try:
                line = self.tempSer.readline().decode()
            except Exception as e:
                self._logger.error(t['error-reading-thermometer'])
                self._logger.exception(str(e))
                continue
            finally:
                self._logger.debug(t['ser-read'].format(str(len(line)), line))
                time.sleep(0.5)

        lastLine = str(line)

        # Clear the serial buffer
        self.tempSer.reset_input_buffer()

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

        self._logger.debug(
            t['thermometer-found'].format(str(start), str(end), lastLine, lastLine[start:end])
        )
        # Make sure that we have a start and an end and that there is something between them
        if start > -1 and end > -1 and end - start > 2:
            try:
                self.lastTemp = float(lastLine[start:end])
                self.nextTempReadingTime = datetime.now() + timedelta(seconds=1)
            except Exception as e:
                self._logger.error(t['temperature-conversion-error'])
                self._logger.error(lastLine[start:end])
                self._logger.exception(str(e))
                self.lastTemp = "-999"
        else:
            self.lastTemp = "-999"
            self._logger.error(t['error-reading-thermometer-specific'].format(lastLine[start:end]))
        self._logger.debug(
            t['temperature-read'].format(str(self.lastTemp))
        )  # + ' ' + str(lastLine))

        return self.lastTemp

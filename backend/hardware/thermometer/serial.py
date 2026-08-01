import time
from datetime import datetime, timedelta

import serial

from hardware.thermometer.base import TempSensor
from hardware.util.exceptions import HardwareLoadError


class SerialTempSensor(TempSensor):
    def __init__(self, thermometer_config: dict):
        """
        Initializes the Serial Thermometer sensor.
        :param thermometer_config:
          dict
            serialDevice
              A string with the device read from
        """
        super().__init__(thermometer_config["id"])
        self.last_temp: float = 0.0
        self.next_temp_reading_time = datetime.now()

        try:
            self.device = serial.Serial(thermometer_config["serialDevice"], timeout=0.5)
        except serial.SerialException as e:
            self.device = None
            raise HardwareLoadError(
                "Thermometer could not be detected at {}, make sure it is plugged in, try another USB port if it is, or change the device name in your lab hardware config file to the correct device name.".format(
                    thermometer_config["serialDevice"]
                )
            ) from e

    def read_sensor(self, max_attempts: int = 10, retry_interval: float = 0.5) -> str:
        for attempt in range(1, max_attempts + 1):
            try:
                reading = self.device.readline().decode("utf-8", errors="ignore")
            except Exception as e:
                self.logger.error(
                    f"{self.t['error-reading-thermometer']} (attempt {attempt}/{max_attempts})"
                )
                self.logger.exception(str(e))
            else:
                self.logger.debug(self.t["ser-read"].format(str(len(reading)), reading))
                if all(token in reading for token in ("\n", "=", ".")):
                    return reading
            time.sleep(retry_interval)

        raise HardwareLoadError(
            f"Thermometer at {self.thermometer_config['serialDevice']} stopped responding after "
            f"{max_attempts} attempts. It may have disconnected or the OS reassigned its device path."
        )

    def get_temp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        Recommended sensor: DS18B20

        A successful read looks something like this: b"t1=+29.06\n"
        It could also have single-digit temperatures
        The loop below looks for the '=' '\n' '.' to detect success

        :return:
            Temperature in Celsius
        """
        if datetime.now() < self.next_temp_reading_time:
            return self.last_temp

        # Read temperature, and afterward clear the serial buffer
        sensor_reading = self.read_sensor()
        self.device.reset_input_buffer()

        # Look for 't1=' or 't=' in the input sensor_reading
        # Unclear why sometimes the thermometer returns 't1=' and other times just 't='
        # Use rfind because we want the last '=' and sometimes input includes extras
        start = sensor_reading.rfind("=") + len("=")

        end = sensor_reading.find("\\n", start)
        if end == -1:
            # Different thermometers may parse differently. These conditionals may need to expand.
            end = sensor_reading.find(" ", start)
        if end == -1:
            # Maybe just go to the end?
            end = len(sensor_reading) - 1

        self.logger.debug(
            self.t["thermometer-found"].format(
                str(start), str(end), sensor_reading, sensor_reading[start:end]
            )
        )
        # Make sure that we have a start and an end and that there is something between them
        if start > -1 and end > -1 and end - start > 2:
            try:
                self.last_temp = float(sensor_reading[start:end])
                self.next_temp_reading_time = datetime.now() + timedelta(seconds=1)
            except Exception as e:
                self.logger.error(self.t["temperature-conversion-error"])
                self.logger.error(sensor_reading[start:end])
                self.logger.exception(str(e))
                self.last_temp = -999.0
        else:
            self.last_temp = -999.0
            self.logger.error(
                self.t["error-reading-thermometer-specific"].format(
                    sensor_reading[start:end]
                )
            )
        self.logger.debug(self.t["temperature-read"].format(str(self.last_temp)))

        return self.last_temp

    def close(self) -> None:
        if self.device:
            self.device.close()

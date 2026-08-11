import time
from datetime import datetime, timedelta
from typing import Optional

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
        self.serial_device = thermometer_config["serialDevice"]
        self.device: Optional[serial.Serial] = None

        try:
            self._connect()
        except serial.SerialException as e:
            raise HardwareLoadError(
                f"Thermometer could not be detected at {self.serial_device}, make sure it is plugged in, try another "
                "USB port if it is, or change the device name in your lab hardware config file to "
                "the correct device name."
            ) from e

    def _connect(self) -> None:
        """(Re)opens the serial connection. Closes any existing handle first."""
        if self.device is not None:
            try:
                self.device.close()
            except serial.SerialException as e:
                # best-effort close of a possibly-dead handle
                self.logger.error(f"Could not close existing Serial thermometer: {e}")
        self.device = serial.Serial(self.serial_device, timeout=0.5)

    def read_sensor(
        self,
        max_attempts: int = 10,
        retry_interval: float = 0.5,
        max_reconnect_attempts: int = 5,
        reconnect_backoff: float = 2.0,
    ) -> str:
        """Read from serial until we get a line containing '\\n', '=' and '.'.
        Attempts a reconnect if the device stops responding entirely."""
        for reconnect_attempt in range(max_reconnect_attempts + 1):
            for attempt in range(1, max_attempts + 1):
                try:
                    reading = self.device.readline().decode("utf-8", errors="ignore")
                except Exception as e:
                    self.logger.error(
                        f"{self.t['error-reading-thermometer']} (attempt {attempt}/{max_attempts})"
                    )
                    self.logger.exception(str(e))
                else:
                    self.logger.debug(
                        self.t["ser-read"].format(str(len(reading)), reading)
                    )
                    if all(token in reading for token in ("\n", "=", ".")):
                        return reading
                time.sleep(retry_interval)

            if reconnect_attempt < max_reconnect_attempts:
                self.logger.error(
                    f"Thermometer at {self.serial_device} unresponsive after {max_attempts} reads; "
                    f"attempting reconnect ({reconnect_attempt + 1}/{max_reconnect_attempts})..."
                )
                try:
                    self._connect()
                except serial.SerialException as e:
                    self.logger.error(f"Reconnect attempt failed: {e}")
                time.sleep(reconnect_backoff)

        raise HardwareLoadError(
            f"Thermometer at {self.serial_device} stopped responding and could not be reconnected "
            f"after {max_reconnect_attempts} attempts. Check the physical USB connection."
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

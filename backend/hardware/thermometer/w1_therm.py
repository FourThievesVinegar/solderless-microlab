from datetime import datetime, timedelta

from w1thermsensor import W1ThermSensor, SensorNotReadyError

from hardware.thermometer.base import TempSensor


class W1TempSensor(TempSensor):

    def __init__(self):
        """
        Initializes the W1ThermSensor.
        """
        super().__init__('W1ThermSensor')

        self.last_temp: float = 0.0
        self.sensor = W1ThermSensor()
        self.next_temp_reading_time = datetime.now()

    def get_temp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        :return:
            Temperature in Celsius
        """
        # With the DS18S20 at least reading new data seems to take ~0.8 seconds,
        # so only read new temp if our temp is over 1 second old to prevent
        # blocking threads for data that hasn't changed much
        if datetime.now() > self.next_temp_reading_time:
            try:
                self.last_temp = self.sensor.get_temperature()
                self.next_temp_reading_time = datetime.now() + timedelta(seconds=1)
            except SensorNotReadyError as e:
                self.logger.debug(f'SensorNotReadyError for {self.device_name}: ', e)
        return self.last_temp

    def close(self) -> None:
        pass

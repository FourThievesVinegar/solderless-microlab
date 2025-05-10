from datetime import datetime, timedelta

from w1thermsensor import W1ThermSensor, SensorNotReadyError

from hardware.thermometer.base import TempSensor


class W1TempSensor(TempSensor):

    def __init__(self):
        """
        Constructor. Initializes the sensor.
        """
        self.lastTemp = 0
        self.sensor = W1ThermSensor()
        self.nextTempReadingTime = datetime.now()

    def getTemp(self) -> float:
        """
        Get the temperature of the sensor in celsius.
        :return:
            Temperature in Celsius
        """
        # With the DS18S20 at least reading new data seems to take ~0.8 seconds,
        # so only read new temp if our temp is over 1 second old to prevent
        # blocking threads for data that hasn't changed much
        if datetime.now() > self.nextTempReadingTime:
            try:
                self.lastTemp = self.sensor.get_temperature()
                self.nextTempReadingTime = datetime.now() + timedelta(seconds=1)
            except SensorNotReadyError:
                pass
        return self.lastTemp

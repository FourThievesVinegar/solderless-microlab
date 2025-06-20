from abc import abstractmethod
from typing import Literal, Optional

from hardware.lab_device import LabDevice
from localization import load_translation


class ReagentDispenser(LabDevice):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)
        self.t = load_translation()

    @abstractmethod
    def dispense(
        self, pump_id: Literal['X', 'Y', 'Z'], volume: float, duration: Optional[float] = None
    ) -> float:
        """
        Dispense reagent.

        :param pump_id: The pump id. One of 'X', 'Y', or 'Z'.
        :param volume: The number of ml to dispense.
        :param duration: Optional - Desired dispense duration in seconds.
        :return: Actual dispense duration in seconds.
        """
        pass

    @abstractmethod
    def get_pump_limits(self, pump_id: Literal['X', 'Y', 'Z']) -> dict[str, float]:
        """
        Get speed limits for the specified pump.

        :param pump_id: The pump id. One of 'X', 'Y', or 'Z'.
        :return: dict with 'minSpeed' and 'maxSpeed' in ml/s.
        """
        pass

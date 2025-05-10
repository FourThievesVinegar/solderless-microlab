from hardware.reagentdispenser.base import ReagentDispenser
from util.logger import MultiprocessingLogger
from localization import load_translation


class SimulatedReagentDispenser(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict):
        self._logger = MultiprocessingLogger.get_logger(__name__)

        self.minSpeed = 0.1
        self.maxSpeed = 10
        if 'minSpeed' in reagent_dispenser_config:
            self.minSpeed = reagent_dispenser_config['minSpeed']
        if 'maxSpeed' in reagent_dispenser_config:
            self.maxSpeed = reagent_dispenser_config['maxSpeed']

    def dispense(self, pumpId: str, volume: int, duration: int = None) -> float:
        """
        Displays pump dispensing message.

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number ml to dispense
        :return:
            None
        """
        t=load_translation()
        
        if pumpId == 'X':
            self._logger.info(t['dispensing-x'].format(volume))
        elif pumpId == 'Y':
            self._logger.info(t['dispensing-y'].format(volume))
        elif pumpId == 'Z':
            self._logger.info(t['dispensing-z'].format(volume))
        else:
            raise ValueError(t['pump-doesnt-exist'].format(pumpId))
        return abs(volume)

    def getPumpSpeedLimits(self, pumpId: str) -> dict:
        return {
            "minSpeed": self.minSpeed,
            "maxSpeed": self.maxSpeed
        }

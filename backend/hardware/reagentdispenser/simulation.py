from hardware.reagentdispenser.base import ReagentDispenser
from util.logger import MultiprocessingLogger


class SimulatedReagentDispenser(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict):
        self._logger = MultiprocessingLogger.get_logger(__name__)

        self.minSpeed = 0.1
        self.maxSpeed = 10
        if 'minSpeed' in reagent_dispenser_config:
            self.minSpeed = reagent_dispenser_config['minSpeed']
        if 'maxSpeed' in reagent_dispenser_config:
            self.maxSpeed = reagent_dispenser_config['maxSpeed']

    def log(self, message):
        self._logger.info('reagentdispenser.simulation - {0}'.format(message))

    def dispense(self, pumpId, volume, duration=None):
        """
        Displays pump dispensing message.

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number ml to dispense
        :return:
            None
        """
        if pumpId == 'X':
            self.log('Dispensing {0}ml from pump X'.format(volume))
        elif pumpId == 'Y':
            self.log('Dispensing {0}ml from pump Y'.format(volume))
        elif pumpId == 'Z':
            self.log('Dispensing {0}ml from pump Z'.format(volume))
        else:
            raise ValueError("Pump '{0}' does not exist.".format(pumpId))
        return abs(volume)

    def getPumpSpeedLimits(self, pumpId):
        return {
            "minSpeed": self.minSpeed,
            "maxSpeed": self.maxSpeed
        }

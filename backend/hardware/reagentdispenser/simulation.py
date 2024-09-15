from hardware.reagentdispenser.base import ReagentDispenser
import time
import logging


def log(message):
    logging.info('reagentdispenser.simulation - {0}'.format(message))


class SimulatedReagentDispenser(ReagentDispenser):
    def __init__(self, args):
        self.minSpeed = 0.1
        self.maxSpeed = 10
        if 'minSpeed' in args:
            self.minSpeed = args['minSpeed'] 
        if 'maxSpeed' in args:
            self.maxSpeed = args['maxSpeed'] 

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
            log('Dispensing {0}ml from pump X'.format(volume))
        elif pumpId == 'Y':
            log('Dispensing {0}ml from pump Y'.format(volume))
        elif pumpId == 'Z':
            log('Dispensing {0}ml from pump Z'.format(volume))
        else:
            raise ValueError("Pump '{0}' does not exist.".format(pumpId))
        return abs(volume)

    def getPumpSpeedLimits(self, pumpId):
        return {
            "minSpeed": self.minSpeed,
            "maxSpeed": self.maxSpeed
        }

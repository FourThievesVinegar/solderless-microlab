from hardware.reagentdispenser.base import ReagentDispenser
import time

def log(message):
    print('reagentdispenser.simulation - {0}'.format(message))

class SimulatedReagentDispenser(ReagentDispenser):

    def dispense(self, pumpId, volume):
        """
        Displays pump dispensing message.

        :param pumpId:
            The pump id. One of 'X' or 'Y'
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
        time.sleep(abs(volume))

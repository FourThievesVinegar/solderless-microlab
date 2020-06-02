from recipes import celery
from recipes import base
import hardware

recipe = base.Recipe(
    {
        'steps': [
            {
                'nr': 0,
                'message': 'Place egg in chamber',
                'options':[{'text':'Done','next':1}],
             },
            {
                'nr': 1,
                'message': 'Add enough water to cover egg',
                'options':[{'text':'Done','next':2}],
            },
            {
                'nr': 2,
                'message': 'How would you like the egg?',
                'options':[{'text':'Hard boiled','next':3},{'text':'Soft boiled','next':6}],
            },
            {
                'nr': 3,
                'message': 'Heating water...',
                'next': 4,
                'baseTask':'heat',
                'parameters':{'temp':100}
            },
            {
                'nr': 4,
                'message': 'Water boiling. Waiting for 2 minutes.',
                # 60s for soft boiled
                'next': 5,
                'baseTask': 'maintain',
                'parameters':{'time':120, 'temp':100, 'tolerance':2, 'type':'heat'}
            },
            {
                'nr': 5,
                'message': 'Egg boiling complete. Might want to wait for the water to cool down.',
                'done': True
            },
            {
                'nr': 6,
                'message': 'Heating water...',
                'next': 7,
                'task': ' heat',
                'parameters': {'temp': 100}
            },
            {
                'nr': 7,
                'message': 'Water boiling. Waiting for 1 minute.',
                # 60s for soft boiled
                'next': 5,
                'baseTask': 'maintainHeat',
                'parameters': {'time': 60, 'temp': 100, 'tolerance': 2}
            }
        ]
    }
)


def heat(parameters):
    targetTemp = parameters['temp']
    celery.logger.info('heating water to ' + str(targetTemp) + '...')
    hardware.turnHeaterOn()
    while hardware.getTemp() < targetTemp:
        hardware.sleep(0.5)


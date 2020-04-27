from recipes import celery
from recipes import base
import hardware

recipe = base.Recipe(
    {
        'steps': [
            {
                'nr':0,
                'message':'Place egg in chamber',
                'options':[{'text':'Done','next':1}],
             },
            {
                'nr':1,
                'message':'Add enough water to cover egg',
                'options':[{'text':'Done','next':2}],
            },
            {
                'nr':2,
                'message':'Heating water...',
                'next':3,
                'task':'heatWater',
                'parameters':{'temp':100}
            },
            {
                'nr': 3,
                'message': 'Water boiling. Waiting for 1 minute.',
            }
        ]
    }
)


def heatWater(parameters):
    celery.logger.info('heating water to ' + str(parameters['temp']) + '...')
    hardware.turnHeatOn()
    hardware.sleep(2)

    #while hardware.

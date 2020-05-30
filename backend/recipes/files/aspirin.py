from recipes import base

recipe = base.Recipe(
    {
        'steps': [
            {
                'nr': 0,
                'message': 'Place 2.0 g salicylic acid in chamber',
                'options':[{'text':'Done','next':1}],
            },
            {
                'nr': 1,
                'message': 'Place XX mL acetic anhydride into Pump A',
                'options':[{'text':'Done','next':2}],
            },
            {
                'nr': 2,
                'message': 'Place XX mL H2SO4 into Pump B',
                'options':[{'text':'Done','next':3}],
            },
            {
                'nr': 3,
                'message': 'Dispensing acetic anhydride...',
                'next': 4,
                'baseTask':' pump',
                'parameters':{'pump':'A','volume': 5},
            },
            {
                'nr': 4,
                'message': 'Dispensing H2SO4...',
                'next': 5,
                'baseTask':' pump',
                'parameters':{'pump':'B','volume': 0.1},
            },
            {
                'nr': 5,
                'message': 'Stirring...',
                'next': 6,
                'baseTask':' stir',
                'parameters':{'time': 30},
            },
            {
                'nr': 6,
                'message': 'Heating solution...',
                'next': 7,
                'baseTask':'heat',
                'parameters':{'temp': 100},
            },
            {
                'nr': 7,
                'message': 'Waiting for 10 minutes.',
                'next': 8,
                'baseTask': 'maintainHeat',
                'parameters':{'time': 600, 'temp': 100, 'tolerance': 2}
            },
            {
                'nr': 8,
                'message': 'Cooling solution...',
                'next': 9,
                'baseTask':'cool',
                'parameters':{'temp': 22},
            },
            {
                'nr': 9,
                'message': 'Crystallizing solution...',
                'next': 10,
                'baseTask':'cool',
                'parameters':{'temp': 5},
            },
            {
                'nr': 10,
                'message': 'Waiting for 10 minutes.',
                'next': 11,
                'baseTask': 'maintainCool',
                'parameters':{'time': 600, 'temp': 5, 'tolerance': 2}
            },
            {
                'nr': 11,
                'message': 'Place 50 mL deionized water into Pump A',
                'options':[{'text':'Done','next':12}],
            },
            {
                'nr': 12,
                'message': 'Dispensing deionized water...',
                'next': 13,
                'baseTask':' pump',
                'parameters':{'pump':'A','volume': 50},
            },
            {
                'nr': 13,
                'message': 'Waiting for 20 minutes.',
                'next': 14,
                'baseTask': 'maintainCool',
                'parameters':{'time': 1200, 'temp': 5, 'tolerance': 2}
            },
            {
                'nr': 14,
                'message': 'Reaction complete. Dry and rinse the product.',
                'done': True
            },
        ]
    }
)


step = 0
message = ''
options = []

#import hardware
#hardware.package = 'simulation'
#from hardware import interface

#interface.heat()

def start():
    global step, message, options
    step = 1
    runStep()

def stop():
    global step, message, options
    step = -1
    message = ''
    options = []

def selectOption(option):
    global step, message, options
    if not option in options:
        return False,'Invalid option ' + option
    else:
        # Can have more complex behaviour here with different goto step 
        # associated with each option
        step = step + 1
        runStep()
        return True,''
    

def runStep():
    global step, message, options
    options = []
    if step == 1:
        message = 'Place egg in chamber'
        options = ['Done']
    elif step == 2:
        message = 'Add enough water to cover egg'
        options = ['Done']
    elif step == 3:
        message = 'Heating water...'
    else:
        message = 'Invalid step'
        return False
    

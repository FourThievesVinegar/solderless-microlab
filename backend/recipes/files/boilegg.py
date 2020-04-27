from recipes import celery
import time


step = 0
message = ''
status = 'idle'
options = []


def start():
    global step, message, options
    step = 1
    runStep()


def stop():
    global step, status, message, options
    step = -1
    status = 'idle'
    message = ''
    options = []


def updateStatus():
    global step, status, message, options
    if step == 3:
        if celery.isTaskComplete():
            step = step + 1
            runStep()
    ret = {
        'status':status,
        'step':step,
        'message':message,
        'options':options
        }
    return ret


def selectOption(option):
    global step, message, options
    if not option in options:
        return False,'Invalid option ' + option
    else:
        # Can have more complex behaviour here with different goto step 
        # associated with each option
        step = step + 1
        if runStep():
            return True,''
        else:
            return False,message


def runStep():
    global step, status, message, options
    options = []
    status = 'running'
    if step == 1:
        status = 'user_input'
        message = 'Place egg in chamber'
        options = ['Done']
    elif step == 2:
        status = 'user_input'
        message = 'Add enough water to cover egg'
        options = ['Done']
    elif step == 3:
        if celery.runTask('heatWater', None):
            message = 'Heating water...'
        else:
            message = 'Internal error. Task already running.'
            return False
    elif step == 4:
        message = 'Water boiling. Waiting for 1 minute.'
    else:
        status = 'error'
        message = 'Invalid step'
        return False
    return True


def heatWater(parameters):
    celery.logger.info('heating water...')
    time.sleep(1)
    return 5

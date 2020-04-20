step = 0

#import hardware
#hardware.package = 'simulation'
#from hardware import interface

#interface.heat()

def getNextStep():
    return step + 1

def runStep(stepNumber):
    global step
    print(stepNumber)
    step = step + 1
    return {'message':'ok','step':step}

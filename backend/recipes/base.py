from recipes import celery

class Recipe:
    step = 0
    message = ''
    status = 'idle'
    options = []

    def __init__(self, plan):
        self.plan = plan


    def start(self):
        self.step = 0
        self.runStep()


    def stop(self):
        self.step = -1
        self.status = 'idle'
        self.message = ''
        self.options = []


    def getStatus(self):
        ret = {
            'status':self.status,
            'step':self.step,
            'message':self.message,
            'options':self.options
        }
        return ret


    def updateStatus(self):
        if self.status == 'running':
            if celery.isTaskComplete():
                self.step = self.plan['steps'][self.step]['next']
                self.runStep()

        return self.getStatus()


    def selectOption(self,optionValue):
        found = False
        for option in self.plan['steps'][self.step]['options']:
            if option['text'] == optionValue:
                self.step = option['next']
                found = True

        if not found:
            return False, 'Invalid option ' + optionValue

        ret = self.runStep()
        return ret,self.message


    def runStep(self):
        step = self.plan['steps'][self.step]
        self.message = step['message']
        options = []

        if 'options' in step:
            for option in step['options']:
                options.append(option['text'])
            if len(options) > 0:
                self.status = 'user_input'

        self.options = options

        if 'task' in step:
            if celery.runTask(step['task'], step['parameters']):
                self.status = 'running'
            else:
                self.status = 'error'
                message = 'Internal error. Task already running.'
                return False

        return True

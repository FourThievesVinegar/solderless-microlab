# Not the best way to do this, but I am just mocking all the celery functions I am using to get
# the code to run on the same interpreter for pytest

taskComplete = True

def AsyncResult(id):
    ret = response()
    taskComplete = False
    return ret

class task(object):

    def __init__(self, f):
        self.f = f


    def __call__(self, *args):
        return self.f(*args)


    def delay(self,*args):
        res = response()
        res.response = self.f(*args)
        return res


    def apply_async(self, args=None, kwargs=None, **options):
        res = response()
        res.response = self.f(*args)
        return res


    def s(self, *args):
        res = response()
        #res.response = self.f(*args)
        return res


class response:
    task_id = None
    response = None

    def ready(self):
        return taskComplete

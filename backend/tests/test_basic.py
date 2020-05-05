import pytest
import os
import api
import json
import config
import time
from tests import celeryMock


@pytest.fixture
def client():
    config.hardwarePackage = 'simulation'
    config.hardwareSpeedup = 10

    config.celeryMode = 'test'

    return api.app.test_client()


def run(client,uri):
    res = client.get(uri)
    assert res.status_code == 200
    message = json.loads(res.data)
    print(message)
    return message


def test_idle(client):
    message = run(client,'/status')
    assert message['recipe'] == None
    assert message['status'] == 'idle'
    assert message['step'] == -1


def test_list(client):
    message = run(client,'/list')
    assert message[0] == 'boilegg'


def test_start_boilegg(client):
    message = run(client,'/start/boilegg')
    assert message['response'] == 'ok'
    message = run(client,'/start/boilegg')
    assert message['response'] == 'error'


def test_hard_boilegg(client):
    message = run(client,'/stop')
    assert message['response'] == 'ok'

    message = run(client,'/start/boilegg')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 0
    assert message['message'] == 'Place egg in chamber'
    assert message['options'][0] == 'Done'
    assert len(message['options']) == 1

    message = run(client,'/select/option/invalid')
    assert message['response'] == 'error'
    assert message['message'] == 'Invalid option invalid'

    message = run(client,'/select/option/Done')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 1
    assert message['message'] == 'Add enough water to cover egg'
    assert message['options'][0] == 'Done'
    assert len(message['options']) == 1

    message = run(client,'/select/option/Done')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 2
    assert message['message'] == 'How would you like the egg?'
    assert message['options'][0] == 'Hard boiled'
    assert message['options'][1] == 'Soft boiled'
    assert len(message['options']) == 2

    message = run(client,'/select/option/Hard boiled')
    assert message['response'] == 'ok'

    celeryMock.taskComplete = False
    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 3
    assert message['message'] == 'Heating water...'
    assert len(message['options']) == 0

    message = run(client,'/select/option/invalid')
    assert message['response'] == 'error'
    assert message['message'] == 'Invalid option invalid'

    celeryMock.taskComplete = True
    startTime = time.time()

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 4
    assert message['message'] == 'Water boiling. Waiting for 2 minutes.'
    assert len(message['options']) == 0

    celeryMock.taskComplete = False
    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 4
    assert message['message'] == 'Water boiling. Waiting for 2 minutes.'
    assert len(message['options']) == 0

    celeryMock.taskComplete = True
    message = run(client,'/status')

    duration = time.time() - startTime
    assert duration > 12
    assert duration < 12.1

    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'complete'
    assert message['step'] == 5
    assert message['message'] == 'Egg boiling complete. Might want to wait for the water to cool down.'
    assert len(message['options']) == 0

    message = run(client,'/start/boilegg')
    assert message['response'] == 'ok'


def test_soft_boilegg(client):
    message = run(client,'/stop')
    assert message['response'] == 'ok'

    message = run(client,'/start/boilegg')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 0
    assert message['message'] == 'Place egg in chamber'
    assert message['options'][0] == 'Done'
    assert len(message['options']) == 1

    message = run(client,'/select/option/invalid')
    assert message['response'] == 'error'
    assert message['message'] == 'Invalid option invalid'

    message = run(client,'/select/option/Done')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 1
    assert message['message'] == 'Add enough water to cover egg'
    assert message['options'][0] == 'Done'
    assert len(message['options']) == 1

    message = run(client,'/select/option/Done')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 2
    assert message['message'] == 'How would you like the egg?'
    assert message['options'][0] == 'Hard boiled'
    assert message['options'][1] == 'Soft boiled'
    assert len(message['options']) == 2

    message = run(client,'/select/option/Soft boiled')
    assert message['response'] == 'ok'

    celeryMock.taskComplete = False
    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 6
    assert message['message'] == 'Heating water...'
    assert len(message['options']) == 0

    celeryMock.taskComplete = True
    startTime = time.time()

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 7
    assert message['message'] == 'Water boiling. Waiting for 1 minute.'
    assert len(message['options']) == 0

    celeryMock.taskComplete = False
    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 7
    assert message['message'] == 'Water boiling. Waiting for 1 minute.'
    assert len(message['options']) == 0

    celeryMock.taskComplete = True
    message = run(client,'/status')

    duration = time.time() - startTime
    assert duration > 6
    assert duration < 6.1

    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'complete'
    assert message['step'] == 5
    assert message['message'] == 'Egg boiling complete. Might want to wait for the water to cool down.'
    assert len(message['options']) == 0

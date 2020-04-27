import pytest
import os
import api
import json
import hardware
import config
from tests import celeryMock

@pytest.fixture
def client():
    hardware.package = 'simulation'
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

def test_boilegg(client):
    message = run(client,'/stop')
    assert message['response'] == 'ok'

    message = run(client,'/start/boilegg')
    assert message['response'] == 'ok'

    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'user_input'
    assert message['step'] == 1
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
    assert message['step'] == 2
    assert message['message'] == 'Add enough water to cover egg'
    assert message['options'][0] == 'Done'
    assert len(message['options']) == 1

    message = run(client,'/select/option/Done')
    assert message['response'] == 'ok'

    celeryMock.taskComplete = False
    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 3
    assert message['message'] == 'Heating water...'
    assert len(message['options']) == 0

    celeryMock.taskComplete = True
    message = run(client,'/status')
    assert message['recipe'] == 'boilegg'
    assert message['status'] == 'running'
    assert message['step'] == 4
    assert message['message'] == 'Water boiling. Waiting for 1 minute.'
    assert len(message['options']) == 0

import pytest
import os
import api
import json

@pytest.fixture
def client():
    return api.app.test_client()

def test_root(client):
    res = client.get('/status')
    assert res.status_code == 200
    message = json.loads(res.data)
    print(message)
    assert message['status'] == 'idle'


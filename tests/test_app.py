import sys
import os
import pytest
from flask import Flask
from app import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_schedule_script(client, monkeypatch):
    class MockTask:
        id = '12345'
        
        def __init__(self, *args, **kwargs):
            pass

    def mock_apply_async(*args, **kwargs):
        return MockTask()

    monkeypatch.setattr('tasks.run_bash_script.apply_async', mock_apply_async)

    response = client.post('/schedule', json={
        'container_name': 'goofy_pascal',
        'script': 'bash /root/Desktop/test1.sh',
        'schedule_time': '2024-07-15T10:00:00'
    })

    assert response.status_code == 202
    assert response.get_json()['task_id'] == '12345'

# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_runtime_info():
    response = client.get("/api/runtime_info")
    assert response.status_code == 200
    data = response.json()
    print(f'\n\ndata: {data}\n\n')
    assert "start_time" in data
    assert "running_time" in data
    assert "total_requests" in data

def test_get_request_statistics():
    response = client.get("/api/request_statistics")
    assert response.status_code == 200
    data = response.json()
    print(f'\n\ndata: {data}\n\n')
    assert isinstance(data, list)

def test_get_task_progress():
    task_id = "task_12345"
    response = client.get(f"/api/task_progress/{task_id}")
    print(f'\n\ndata: {response}\n\n')
    assert response.status_code in [200, 404]  # 可能返回的状态码

def test_get_error_logs():
    response = client.get("/api/error_logs")
    assert response.status_code == 200
    data = response.json()
    print(f'\n\ndata: {data}\n\n')
    assert isinstance(data, list)

def test_post_manual_retry():
    response = client.post("/api/manual_retry", json={"task_id": "task_12345", "retry_count": 3})
    print(f'\n\ndata: {response}\n\n')
    assert response.status_code == 200
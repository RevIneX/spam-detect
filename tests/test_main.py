import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_spam():
    response = client.post("/analyze", json={"text": "Hey! You won a ten million dollars! Click here!"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "score" in data
    assert data["result"] in ["SPAM", "HAM"]

def test_analyze_ham():
    response = client.post("/analyze", json={"text": "Hello, how are you? Let's meet tomorrow."})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "score" in data

def test_analyze_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_analyze_too_long():
    long_text = "a" * 600
    response = client.post("/analyze", json={"text": long_text})
    assert response.status_code == 400
    assert "too long" in response.json()["detail"].lower()

def test_get_history():
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_history_with_pagination():
    response = client.get("/history?page=1&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_history_item_not_found():
    response = client.get("/history/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

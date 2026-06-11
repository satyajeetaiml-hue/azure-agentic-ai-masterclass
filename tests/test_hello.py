"""Tests for the Week 1 helpdesk triage agent."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_hello_answers_from_kb():
    resp = client.post("/api/v1/hello", json={"message": "I forgot my password"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["category"] == "password"
    assert body["escalated"] is False
    assert len(body["steps"]) >= 4  # reason, plan, act, observe


def test_hello_escalates_on_urgency():
    resp = client.post(
        "/api/v1/hello",
        json={"message": "Production is down, this is urgent!"},
    )
    assert resp.status_code == 200
    assert resp.json()["escalated"] is True


def test_hello_validates_empty_message():
    resp = client.post("/api/v1/hello", json={"message": ""})
    assert resp.status_code == 422

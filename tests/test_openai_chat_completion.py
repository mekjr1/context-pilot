from fastapi.testclient import TestClient
from contextpilot.main import app
from contextpilot.storage.repositories import list_traces

HEADERS = {"x-api-key": "local-dev-key"}


def test_models():
    assert TestClient(app).get("/v1/models", headers=HEADERS).status_code == 200


def test_chat():
    response = TestClient(app).post(
        "/v1/chat/completions",
        json={"model": "contextpilot-auto", "messages": [{"role": "user", "content": "hi"}]},
        headers=HEADERS,
    )
    assert response.status_code == 200


def test_stream():
    response = TestClient(app).post(
        "/v1/chat/completions",
        json={
            "model": "contextpilot-auto",
            "messages": [{"role": "user", "content": "hi"}],
            "stream": True,
        },
        headers=HEADERS,
    )
    assert response.status_code == 200


def test_trace_payload_redacts_sensitive_fields():
    client = TestClient(app)
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "contextpilot-auto",
            "messages": [{"role": "user", "content": "hi"}],
            "tools": [{"type": "function", "api_key": "super-secret"}],
        },
        headers=HEADERS,
    )
    assert response.status_code == 200
    traces = list_traces(limit=1)
    assert traces
    row = traces[0]
    assert "***REDACTED***" in row.payload

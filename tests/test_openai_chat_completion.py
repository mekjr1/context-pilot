from fastapi.testclient import TestClient
from contextpilot.main import app


def test_models():
    assert TestClient(app).get("/v1/models").status_code == 200


def test_chat():
    response = TestClient(app).post(
        "/v1/chat/completions",
        json={"model": "contextpilot-auto", "messages": [{"role": "user", "content": "hi"}]},
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
    )
    assert response.status_code == 200

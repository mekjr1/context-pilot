from fastapi.testclient import TestClient

from contextpilot.main import app


def test_models(auth_headers):
    assert TestClient(app).get("/v1/models", headers=auth_headers).status_code == 200


def test_chat(auth_headers):
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={"model": "contextpilot-auto", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert response.status_code == 200


def test_stream(auth_headers):
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={
            "model": "contextpilot-auto",
            "messages": [{"role": "user", "content": "hi"}],
            "stream": True,
        },
    )
    assert response.status_code == 200

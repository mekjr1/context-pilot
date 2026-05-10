from fastapi.testclient import TestClient

from contextpilot.main import app


def _auth_headers():
    return {"Authorization": "Bearer local-dev-key"}


def test_models():
    assert TestClient(app).get("/v1/models", headers=_auth_headers()).status_code == 200


def test_chat():
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=_auth_headers(),
        json={"model": "contextpilot-auto", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert response.status_code == 200


def test_stream():
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=_auth_headers(),
        json={
            "model": "contextpilot-auto",
            "messages": [{"role": "user", "content": "hi"}],
            "stream": True,
        },
    )
    assert response.status_code == 200

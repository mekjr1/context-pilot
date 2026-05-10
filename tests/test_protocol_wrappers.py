from fastapi.testclient import TestClient

from contextpilot.main import app


def _auth_headers():
    return {"Authorization": "Bearer local-dev-key"}


def test_responses_wrapper():
    client = TestClient(app)
    response = client.post(
        "/v1/responses",
        headers=_auth_headers(),
        json={"model": "contextpilot-auto", "input": "hello"},
    )
    assert response.status_code == 200


def test_anthropic_messages_wrapper():
    client = TestClient(app)
    response = client.post(
        "/v1/messages",
        headers=_auth_headers(),
        json={"model": "contextpilot-auto", "messages": [{"role": "user", "content": "hello"}]},
    )
    assert response.status_code == 200
    assert response.json()["type"] == "message"

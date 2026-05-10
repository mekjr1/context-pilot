from fastapi.testclient import TestClient

from contextpilot.main import app

HEADERS = {"x-api-key": "local-dev-key"}


def test_responses_wrapper():
    client = TestClient(app)
    response = client.post(
        "/v1/responses",
        json={"model": "contextpilot-auto", "input": "hello"},
        headers=HEADERS,
    )
    assert response.status_code == 200


def test_anthropic_messages_wrapper():
    client = TestClient(app)
    response = client.post(
        "/v1/messages",
        json={"model": "contextpilot-auto", "messages": [{"role": "user", "content": "hello"}]},
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert response.json()["type"] == "message"

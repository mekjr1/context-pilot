from fastapi.testclient import TestClient

from contextpilot.main import app


def test_v1_requires_api_key():
    response = TestClient(app).get("/v1/models")
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid API key"


def test_validation_errors_are_standardized():
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers={"x-api-key": "local-dev-key"},
        json={"model": "contextpilot-auto", "messages": "bad"},
    )
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["type"] == "invalid_request_error"

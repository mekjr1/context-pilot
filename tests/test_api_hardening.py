from fastapi.testclient import TestClient

from contextpilot.main import app
from contextpilot.storage.repositories import list_traces


def _auth_headers():
    return {"Authorization": "Bearer local-dev-key"}


def test_auth_is_enforced_on_v1_routes():
    response = TestClient(app).get("/v1/models")
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["type"] == "unauthorized_error"


def test_validation_errors_are_standardized():
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=_auth_headers(),
        json={"model": "contextpilot-auto", "messages": "invalid"},
    )
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["type"] == "invalid_request_error"


def test_trace_payload_redaction():
    marker = "safe-visible-marker"
    secret = "super-secret-value"
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=_auth_headers(),
        json={
            "model": "contextpilot-auto",
            "messages": [{"role": "user", "content": "hi"}],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "probe",
                        "arguments": {"note": marker, "api_key": secret},
                    },
                }
            ],
        },
    )
    assert response.status_code == 200

    traces = list_traces(limit=50)
    match = next((trace for trace in traces if marker in trace.payload), None)
    assert match is not None
    assert secret not in match.payload
    assert "[REDACTED]" in match.payload

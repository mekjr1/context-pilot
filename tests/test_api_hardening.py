import uuid

from fastapi.testclient import TestClient

from contextpilot.main import app
from contextpilot.storage.repositories import list_traces

TRACE_SCAN_LIMIT = 200


def test_auth_is_enforced_on_v1_routes():
    response = TestClient(app).get("/v1/models")
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["type"] == "unauthorized_error"


def test_validation_errors_are_standardized(auth_headers):
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={"model": "contextpilot-auto", "messages": "invalid"},
    )
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["type"] == "invalid_request_error"


def test_trace_payload_redaction(auth_headers):
    marker = f"safe-visible-marker-{uuid.uuid4()}"
    secret = "super-secret-value"
    response = TestClient(app).post(
        "/v1/chat/completions",
        headers=auth_headers,
        json={
            "model": "contextpilot-auto",
            "messages": [{"role": "user", "content": "hi"}],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "probe",
                        "parameters": {"note": marker, "api_key": secret},
                    },
                }
            ],
        },
    )
    assert response.status_code == 200

    traces = list_traces(limit=TRACE_SCAN_LIMIT)
    match = next((trace for trace in traces if marker in trace.payload), None)
    assert match is not None
    assert secret not in match.payload
    assert "[REDACTED]" in match.payload

# Security

- Local-first by default; no forced cloud dependency.
- `/v1/*` endpoints enforce API key authentication (`x-api-key` or Bearer token).
- Error responses are normalized to a consistent `{"error": ...}` structure.
- Trace persistence sanitizes payloads and redacts sensitive keys (for example: `api_key`, `authorization`, `token`, `secret`, `password`).
- External-doc freshness checks can be allowlisted in future phases.
- Prompt injection risk exists for any external docs ingestion path.
- Memory pollution is controlled by explicit memory-write tool calls.
- Trace logging provides auditability of route decisions.

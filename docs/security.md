# Security

- Local-first by default; no forced cloud dependency.
- API key enforcement is active for `/v1/*` endpoints (health remains open).
- External-doc freshness checks can be allowlisted in future phases.
- Trace payloads are redacted for common secret-bearing keys (`api_key`, `token`, `secret`, `password`, `authorization`).
- Prompt injection risk exists for any external docs ingestion path.
- Memory pollution is controlled by explicit memory-write tool calls.
- Trace logging provides auditability of route decisions.

# Security

- Local-first by default; no forced cloud dependency.
- External-doc freshness checks can be allowlisted in future phases.
- Avoid logging secrets in traces/payloads in production deployment.
- Prompt injection risk exists for any external docs ingestion path.
- Memory pollution is controlled by explicit memory-write tool calls.
- Trace logging provides auditability of route decisions.

# ContextPilot

ContextPilot is a local-first smart model gateway and MCP-ready control plane for coding agents.

## Production readiness status
This repository now includes a hardened MVP implementation with typed APIs, routing policies, persistence, and test scaffolding. It is ready for internal/self-hosted use and extension, but still intentionally limits provider integrations to Echo by default.

## Features
- FastAPI server with:
  - `GET /health`
  - `GET /v1/models`
  - `POST /v1/chat/completions`
  - `POST /v1/responses` (compat wrapper)
  - `POST /v1/messages` (Anthropic-style adapter)
- Deterministic task classifier + policy model routing
- Context planning strategy output
- SSE streaming for chat completions
- SQLite persistence for traces, route decisions, memories, freshness checks
- Repo indexing/search scaffold with metadata and ignore rules
- Freshness checks for web URL/local file/git-repo stub
- Typer CLI for serve/classify/plan/index/search/freshness/traces

## Install
```bash
pip install -e .
```

## Run
```bash
contextpilot serve --host 127.0.0.1 --port 8787
```

## CLI
```bash
contextpilot classify "Fix retry bug in webhook handler"
contextpilot plan "Use latest API docs for migration"
contextpilot add-repo .
contextpilot index-repo .
contextpilot search-repo "retry" .
contextpilot check-source https://docs.stripe.com/webhooks
contextpilot traces
```

## Integrations
See `examples/` for Continue/Aider/Claude Code/Copilot CLI environment samples.

## Security notes
See `docs/security.md` for threat model and controls.

## Reality check before continuing development

This project is a strong MVP scaffold, but it is **not full production-ready yet**.

### What works today
- Typed API contracts and protocol wrappers for OpenAI-style and Anthropic-style requests.
- Deterministic classify -> route -> plan flow with trace persistence.
- SQLite-backed traces, route decisions, memories, and freshness events.
- Local-first CLI and repository indexing/search scaffolds.

### What still needs to be done for production
1. Enforce API auth at request boundaries (current API key config is not enforced in middleware/dependencies).
2. Add robust error handling and standardized error payloads across provider/database/network failures.
3. Add secret redaction and safer payload logging (current traces can include raw request content).
4. Add migration versioning and operational DB lifecycle controls.
5. Add real provider integrations (OpenAI/Anthropic/LiteLLM), retries, timeouts, and failover.
6. Add rate limits, stronger security controls, and deployment hardening.

### Environment note
In this execution environment, installation and runtime tests were blocked by package index/network restrictions (dependency downloads fail), so use a normal Python environment for full install-and-run validation.

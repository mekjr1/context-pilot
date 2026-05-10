# ContextPilot Codex Handoff

## Task: Scaffold ContextPilot, a smart backend model endpoint and MCP control plane for AI coding agents

You are building the first working scaffold of **ContextPilot**.

ContextPilot is a local-first smart model gateway for AI coding agents. It can be configured as the backend model endpoint for tools like Continue, Aider, Claude Code, Copilot CLI, and custom agents. It also exposes an MCP server so host agents can call ContextPilot before bloating prompts with repo/docs context.

The product goal:

> Use your normal AI coding tool. Point the model endpoint to ContextPilot. It will classify the task, decide whether repo/docs/memory/RAG are needed, route to the right model, check source freshness, inject compact context, stream the response, and log cost/token/route traces.

---

## Build philosophy

Do not overbuild. This is an MVP scaffold, not the final product.

Prioritize:

- Clean architecture
- Protocol compatibility
- Local-first operation
- Easy extension
- Testability
- Simple provider abstraction
- Clear docs

Avoid:

- Full SaaS
- Complex UI
- Multi-tenant auth
- Real billing
- Deep autonomous agent execution
- Heavy vector DB dependencies unless optional

---

## Tech stack

Use Python.

Preferred stack:

- FastAPI
- Uvicorn
- Pydantic v2
- httpx
- SQLite via SQLAlchemy or SQLModel
- Typer for CLI
- pytest
- ruff
- mypy optional
- LiteLLM integration as optional/provider layer
- MCP server support via a lightweight Python MCP implementation if available; otherwise scaffold the interface cleanly

Local vector support:

- Start with a stub interface.
- Add optional sqlite-vec support if practical.
- Do not make vector search mandatory for first boot.

---

## Required repository structure

```text
contextpilot/
  pyproject.toml
  README.md
  .env.example
  .gitignore
  src/
    contextpilot/
      __init__.py
      main.py
      config.py
      logging.py

      api/
        __init__.py
        openai.py
        anthropic.py
        health.py
        models.py

      gateway/
        __init__.py
        normalizer.py
        streamer.py
        errors.py
        usage.py

      router/
        __init__.py
        classifier.py
        policies.py
        model_router.py
        schemas.py

      context/
        __init__.py
        planner.py
        pack_builder.py
        repo_indexer.py
        docs_fetcher.py
        freshness.py
        memory.py

      storage/
        __init__.py
        db.py
        models.py
        repositories.py
        migrations.py

      providers/
        __init__.py
        base.py
        echo.py
        openai_compatible.py
        litellm_provider.py

      mcp/
        __init__.py
        server.py
        tools.py
        schemas.py

      cli/
        __init__.py
        app.py

  tests/
    test_health.py
    test_openai_chat_completion.py
    test_router_classifier.py
    test_context_planner.py
    test_freshness.py

  examples/
    continue.config.yaml
    aider.env.example
    claude-code.env.example
    copilot-cli.env.example
    copilot-instructions.md
    contextpilot.skill.md

  docs/
    architecture.md
    roadmap.md
    protocols.md
    security.md
```

---

# Required features for MVP

## 1. FastAPI server

Create a local server that runs with:

```bash
contextpilot serve --host 127.0.0.1 --port 8787
```

Also allow:

```bash
uvicorn contextpilot.main:app --reload --port 8787
```

Required endpoints:

```text
GET  /health
GET  /v1/models
POST /v1/chat/completions
POST /v1/responses
POST /v1/messages
```

For MVP:

- `/v1/chat/completions` must be functional.
- `/v1/responses` can be a compatibility wrapper or stub with clear TODO.
- `/v1/messages` can support a minimal Anthropic-style request/response or stub with clear TODO.

---

## 2. OpenAI-compatible chat completions

Implement enough of `/v1/chat/completions` to work with OpenAI-compatible clients.

Support:

- `model`
- `messages`
- `stream`
- `temperature`
- `max_tokens`
- basic tool/function fields pass-through if present

For the first scaffold, include an `EchoProvider` that returns a deterministic fake response so tests can pass without external API keys.

Response should look like an OpenAI-compatible response.

Streaming:

- Implement basic Server-Sent Events streaming for `stream=true`.
- It can stream mock chunks in the EchoProvider.
- Design the streaming abstraction so real providers can be plugged in later.

---

## 3. Request classification

Implement a lightweight task classifier.

Input:

- messages
- model requested
- optional metadata

Output schema:

```json
{
  "task_type": "trivial|code_explanation|code_fix|architecture|docs_lookup|research|unknown",
  "complexity": "trivial|easy|medium|hard|deep",
  "needs_codebase": true,
  "needs_external_docs": false,
  "needs_memory": true,
  "freshness_required": false,
  "recommended_model_tier": "cheap|default|strong|deep",
  "confidence": 0.0
}
```

For MVP, use deterministic heuristics first:

- mentions `fix`, `bug`, `test`, `refactor` => code-related
- mentions `repo`, `codebase`, `file`, `function`, `class` => needs_codebase
- mentions `latest`, `docs`, `API`, `version`, `current` => needs_external_docs and freshness_required
- long prompts or architecture words => higher complexity
- simple definition/explanation => cheap/default

Do not call an LLM for classification in the first scaffold unless behind an optional interface.

---

## 4. Policy-based model routing

Create model routing policies in config.

Example config:

```yaml
models:
  cheap:
    provider: echo
    model: echo-small

  default:
    provider: echo
    model: echo-default

  strong:
    provider: echo
    model: echo-strong

  deep:
    provider: echo
    model: echo-deep

routes:
  trivial:
    model_tier: cheap
  code_fix:
    model_tier: default
  architecture:
    model_tier: strong
  research:
    model_tier: strong
```

The model router should select a provider/model based on classifier output.

---

## 5. Context planner

Implement a `ContextPlanner`.

Input:

- classification
- user messages
- workspace path if provided
- model budget policy

Output:

```json
{
  "strategy": "direct|memory_only|repo_search|docs_freshness|repo_and_docs|deep_agent",
  "steps": [],
  "do_not_do": [],
  "recommended_context_limit_tokens": 4000
}
```

For MVP, it can return strategy and steps without doing heavy retrieval.

Example behavior:

- trivial => direct
- code_fix + needs_codebase => repo_search
- docs_lookup + freshness_required => docs_freshness
- architecture + needs_codebase + docs => repo_and_docs

---

## 6. Local storage

Create SQLite schema for:

- sources
- artifacts
- chunks
- memories
- traces
- route_decisions
- freshness_checks

Use SQLAlchemy or SQLModel.

For MVP, implement:

- database initialization
- create tables on startup
- write trace for each request
- store route decision
- simple memory insert/retrieve APIs

---

## 7. Freshness checker

Implement source freshness abstraction.

Support MVP source types:

- `web_url`
- `git_repo`
- `local_file`

For MVP:

- web URL: HEAD request, store ETag and Last-Modified when available
- local file: content hash and mtime
- git repo: stub interface that records remote URL/branch/commit if provided

Do not build a crawler yet.

---

## 8. Repo indexer scaffold

Implement repo indexer interface.

For MVP:

- walk a local repo
- ignore `.git`, `node_modules`, `.venv`, `__pycache__`, `vendor`, `dist`, `build`
- collect file metadata
- optionally read small text files
- store path, language guess, hash, size
- do not embed everything yet

CLI commands:

```bash
contextpilot add-repo .
contextpilot index-repo .
contextpilot search-repo "webhook retry"
```

Search can be basic substring search for MVP.

---

## 9. MCP server scaffold

Create MCP tool definitions for:

- `contextpilot.plan_request`
- `contextpilot.get_context_pack`
- `contextpilot.search_repo`
- `contextpilot.check_freshness`
- `contextpilot.fetch_and_index_source`
- `contextpilot.retrieve_memory`
- `contextpilot.store_memory`
- `contextpilot.explain_route`

If full MCP implementation is too much for the first pass:

- create a clean module with schemas and callable functions
- document how to expose them over MCP in the next phase
- keep the code ready for real MCP server wiring

---

## 10. CLI

Implement Typer CLI:

```bash
contextpilot serve
contextpilot classify "Fix the Stripe webhook retry bug"
contextpilot plan "Fix the Stripe webhook retry bug"
contextpilot add-repo .
contextpilot index-repo .
contextpilot check-source https://docs.stripe.com/webhooks
contextpilot models
contextpilot traces
```

---

## 11. Example integrations

Create example config files.

### Continue

`examples/continue.config.yaml`

```yaml
name: ContextPilot
version: 0.0.1
schema: v1

models:
  - name: ContextPilot Auto
    provider: openai
    model: contextpilot-auto
    apiBase: http://localhost:8787/v1
    apiKey: local-dev-key
```

### Aider

`examples/aider.env.example`

```bash
export OPENAI_API_BASE=http://localhost:8787/v1
export OPENAI_API_KEY=local-dev-key
```

### Claude Code

`examples/claude-code.env.example`

```bash
export ANTHROPIC_BASE_URL=http://localhost:8787
export ANTHROPIC_AUTH_TOKEN=local-dev-key
```

### Copilot CLI

`examples/copilot-cli.env.example`

```bash
export COPILOT_PROVIDER_TYPE=openai
export COPILOT_PROVIDER_BASE_URL=http://localhost:8787/v1
export COPILOT_PROVIDER_API_KEY=local-dev-key
export COPILOT_MODEL=contextpilot-auto
```

---

## 12. Skill / instruction pack

Create:

`examples/copilot-instructions.md`

Content:

```md
Before answering any non-trivial coding, architecture, debugging, refactoring, documentation, dependency, or codebase question, call the ContextPilot MCP tool `contextpilot.plan_request` first and follow the returned routing/context plan unless it is unavailable or unsafe.

Do not read large parts of the repository before asking ContextPilot for a context plan. Prefer ContextPilot-provided context packs over broad file reads.
```

Create:

`examples/contextpilot.skill.md`

Content should include:

- skill name
- when to use
- tool usage order
- warning not to over-read repo
- memory write rules
- freshness checking rules

Suggested content:

```md
---
name: contextpilot
description: Use ContextPilot before solving coding, debugging, architecture, documentation, dependency, RAG, or codebase tasks. It routes tasks, checks freshness, retrieves minimal context, and reduces token usage.
---

# ContextPilot Skill

Before performing a non-trivial task, call the ContextPilot MCP server.

Use:

1. `contextpilot.plan_request` to classify the task.
2. `contextpilot.get_context_pack` to retrieve minimal repo or docs context.
3. `contextpilot.check_freshness` before relying on cached external docs.
4. `contextpilot.store_memory` only for durable repo facts, decisions, or reusable lessons.
5. `contextpilot.explain_route` when the user asks why a model/tool/source was used.

Do not load large files, broad folders, or external docs before asking ContextPilot for a routing plan.
```

---

## 13. Tests

Add pytest tests for:

- `/health`
- `/v1/models`
- non-streaming `/v1/chat/completions`
- streaming `/v1/chat/completions`
- task classifier
- context planner
- SQLite trace write
- freshness checker for local file
- repo indexer ignoring common directories

---

## 14. Documentation

Create `README.md`.

Include:

- what ContextPilot is
- why backend model endpoint + MCP hybrid matters
- installation
- run server
- run CLI
- examples for Continue/Aider/Claude Code/Copilot CLI
- current limitations
- roadmap

Create `docs/architecture.md`.

Include:

- runtime diagram
- request flow
- components
- provider strategy
- MCP strategy

Create `docs/protocols.md`.

Include:

- OpenAI compatibility goals
- Anthropic compatibility goals
- streaming behavior
- tool call behavior
- known gaps

Create `docs/security.md`.

Include:

- local-first stance
- source allowlists
- secret leakage risk
- prompt injection risk from docs
- memory pollution
- tool execution restrictions
- audit traces

Create `docs/roadmap.md`.

Include phases:

### Phase 1

- local gateway
- simple classifier
- echo provider
- SQLite
- CLI
- tests

### Phase 2

- LiteLLM provider
- real OpenAI/Anthropic providers
- real MCP server
- repo search improvements
- docs freshness

### Phase 3

- vector search
- reranking
- memory policies
- Langfuse integration
- route evaluation

### Phase 4

- Claude Code hooks
- Copilot custom agent pack
- team mode
- admin dashboard

---

# Acceptance criteria

The scaffold is acceptable when:

1. `pip install -e .` works.
2. `contextpilot serve` starts the server.
3. `GET /health` returns OK.
4. `GET /v1/models` returns at least `contextpilot-auto`.
5. `POST /v1/chat/completions` returns OpenAI-compatible JSON.
6. `POST /v1/chat/completions` with `stream=true` returns SSE-style chunks.
7. `contextpilot classify "Fix the Stripe webhook retry bug"` returns a code_fix-style classification.
8. `contextpilot plan "Use the latest Stripe webhook docs"` returns docs freshness strategy.
9. SQLite DB is created locally.
10. Each request writes a trace/route decision.
11. Tests pass.
12. README explains how to point Continue/Aider/Claude Code/Copilot CLI to the local gateway.

---

# Do not implement yet

Do not implement:

- real SaaS auth
- paid billing
- production dashboards
- complex vector DB setup
- full autonomous code editing
- cloud deployment
- browser UI

Keep the scaffold clean, testable, and easy to extend.

---

# Suggested first Codex instruction

Paste this before the task brief when using Codex:

```md
Create a new branch called `scaffold/contextpilot-mvp`.

Implement the MVP scaffold described below. Make small, reviewable commits. After implementation, run tests and update the README with exact run commands. Do not add heavy dependencies unless needed. Prefer working code with clear extension points over ambitious incomplete abstractions.
```

---

# Important implementation note

The most practical first target is **not native Copilot IDE Chat**.

The easiest proof points are:

1. Continue via OpenAI-compatible `apiBase`
2. Aider via OpenAI-compatible endpoint
3. Claude Code via Anthropic-compatible gateway
4. Copilot CLI via BYOK/custom OpenAI-compatible endpoint

This avoids betting the first MVP on a surface that may not expose full backend model replacement.

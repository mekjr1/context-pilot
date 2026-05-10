# Architecture

## Runtime flow
1. Client sends request to ContextPilot gateway.
2. Classifier infers task type/complexity.
3. Model router maps classification to a model tier.
4. Context planner proposes retrieval strategy.
5. Provider executes (Echo in MVP) and streams/returns response.
6. Trace + route decision persist to SQLite.

## Components
- `api/`: protocol adapters.
- `router/`: classify + route policy.
- `context/`: planning, freshness, indexing.
- `providers/`: provider abstraction and implementations.
- `storage/`: SQLite persistence.
- `mcp/`: MCP tool/schema/server scaffolds.

# Protocols

## OpenAI compatibility goals
- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/responses` compatibility wrapper (MVP TODO)

## Anthropic compatibility goals
- `POST /v1/messages` minimal compatibility response.

## Streaming
- SSE with `data:` chunks and terminal `[DONE]`.

## Known gaps
- Real tool-call execution and advanced response formats are not yet implemented.

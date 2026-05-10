from typing import Any

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: Any


class ChatCompletionRequest(BaseModel):
    model: str = "contextpilot-auto"
    messages: list[ChatMessage] = Field(default_factory=list)
    stream: bool = False
    temperature: float | None = None
    max_tokens: int | None = None
    tools: list[dict[str, Any]] | None = None


class ResponsesRequest(BaseModel):
    model: str = "contextpilot-auto"
    input: Any
    stream: bool = False


class AnthropicMessagesRequest(BaseModel):
    model: str = "contextpilot-auto"
    messages: list[ChatMessage] = Field(default_factory=list)
    max_tokens: int | None = None

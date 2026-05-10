from fastapi import APIRouter, Depends

from contextpilot.api.openai import chat
from contextpilot.api.auth import require_api_key
from contextpilot.api.schemas import AnthropicMessagesRequest, ChatCompletionRequest

router = APIRouter(prefix="/v1", dependencies=[Depends(require_api_key)])


@router.post("/messages")
def messages(req: AnthropicMessagesRequest):
    proxy = ChatCompletionRequest(model=req.model, messages=req.messages, stream=False)
    response = chat(proxy)
    text = response["choices"][0]["message"]["content"]
    return {
        "id": "msg_contextpilot_1",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": text}],
        "model": req.model,
    }

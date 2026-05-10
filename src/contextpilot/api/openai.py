import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from contextpilot.api.schemas import ChatCompletionRequest, ResponsesRequest
from contextpilot.context.planner import plan
from contextpilot.router.classifier import classify
from contextpilot.router.model_router import select_model
from contextpilot.storage.repositories import write_route, write_trace

router = APIRouter(prefix="/v1")


@router.post("/chat/completions")
def chat(req: ChatCompletionRequest):
    payload = req.model_dump()
    messages = [m.model_dump() for m in req.messages]
    classification = classify(messages, req.model)
    route = select_model(classification)
    write_route(classification.task_type, route["tier"])
    write_trace(classification.task_type, json.dumps(payload))

    provider = route["provider"]
    model = route["model"]

    if req.stream:
        def stream_gen():
            for chunk in provider.stream(model, messages):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_gen(), media_type="text/event-stream")

    response = provider.complete(model, messages)
    response["contextpilot"] = {
        "classification": classification.model_dump(),
        "plan": plan(classification, messages=messages),
    }
    return response


@router.post("/responses")
def responses(req: ResponsesRequest):
    input_value = req.input if isinstance(req.input, str) else json.dumps(req.input)
    faux = ChatCompletionRequest(
        model=req.model,
        messages=[{"role": "user", "content": input_value}],
        stream=req.stream,
    )
    return chat(faux)

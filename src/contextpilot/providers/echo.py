import json
from .base import Provider

class EchoProvider(Provider):
    def complete(self, model:str, messages:list, **kwargs):
        content = f"echo:{messages[-1].get('content','')}" if messages else "echo:"
        return {"id":"chatcmpl-echo","object":"chat.completion","model":model,"choices":[{"index":0,"message":{"role":"assistant","content":content},"finish_reason":"stop"}],"usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}}

    def stream(self, model:str, messages:list, **kwargs):
        text=f"echo:{messages[-1].get('content','')}" if messages else "echo:"
        for ch in [text[:max(1,len(text)//2)], text[max(1,len(text)//2):]]:
            yield json.dumps({"id":"chatcmpl-echo","object":"chat.completion.chunk","model":model,"choices":[{"index":0,"delta":{"content":ch},"finish_reason":None}]})
        yield json.dumps({"id":"chatcmpl-echo","object":"chat.completion.chunk","model":model,"choices":[{"index":0,"delta":{},"finish_reason":"stop"}]})

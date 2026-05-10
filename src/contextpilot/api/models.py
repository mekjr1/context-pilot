from fastapi import APIRouter, Depends

from contextpilot.api.auth import require_api_key

router = APIRouter(prefix="/v1", dependencies=[Depends(require_api_key)])


@router.get("/models")
def models():
    return {"object": "list", "data": [{"id": "contextpilot-auto", "object": "model"}]}

from fastapi import APIRouter
router=APIRouter(prefix="/v1")
@router.get("/models")
def models(): return {"object":"list","data":[{"id":"contextpilot-auto","object":"model"}]}

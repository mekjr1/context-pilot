import hmac

from fastapi import Header, HTTPException

from contextpilot.config import settings


def _extract_api_key(
    authorization: str | None, x_api_key_header: str | None
) -> str | None:
    if x_api_key_header:
        return x_api_key_header
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token


def require_api_key(
    authorization: str | None = Header(default=None),
    x_api_key_header: str | None = Header(default=None, alias="x-api-key"),
) -> None:
    if not settings.api_key:
        return
    token = _extract_api_key(
        authorization=authorization, x_api_key_header=x_api_key_header
    )
    if not token or not hmac.compare_digest(token, settings.api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

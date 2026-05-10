from pydantic import BaseModel, Field


class ModelRoute(BaseModel):
    provider: str
    model: str


class Settings(BaseModel):
    db_url: str = Field(default="sqlite:///contextpilot.db")
    api_key: str = Field(default="local-dev-key")
    models: dict[str, ModelRoute] = Field(
        default_factory=lambda: {
            "cheap": ModelRoute(provider="echo", model="echo-small"),
            "default": ModelRoute(provider="echo", model="echo-default"),
            "strong": ModelRoute(provider="echo", model="echo-strong"),
            "deep": ModelRoute(provider="echo", model="echo-deep"),
        }
    )
    routes: dict[str, str] = Field(
        default_factory=lambda: {
            "trivial": "cheap",
            "code_fix": "default",
            "architecture": "strong",
            "research": "strong",
            "docs_lookup": "default",
            "unknown": "cheap",
        }
    )


settings = Settings()

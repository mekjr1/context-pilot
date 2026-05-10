from contextpilot.config import settings
from contextpilot.providers.echo import EchoProvider


def select_model(classification):
    tier = settings.routes.get(classification.task_type, classification.recommended_model_tier)
    route = settings.models.get(tier, settings.models["default"])
    if route.provider == "echo":
        provider = EchoProvider()
    else:
        provider = EchoProvider()
    return {"provider": provider, "model": route.model, "tier": tier}

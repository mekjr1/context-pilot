SENSITIVE_KEY_PARTS = ("api_key", "apikey", "token", "secret", "password", "authorization")


def redact_payload(value):
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            if any(part in key.lower() for part in SENSITIVE_KEY_PARTS):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_payload(item)
        return redacted
    if isinstance(value, list):
        return [redact_payload(item) for item in value]
    return value

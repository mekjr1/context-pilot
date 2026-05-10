SENSITIVE_KEYWORDS = {"api_key", "authorization", "token", "secret", "password"}
REDACTED_VALUE = "***REDACTED***"


def sanitize_for_trace(
    payload,
    *,
    max_depth: int = 6,
    max_items: int = 100,
    max_string_length: int = 1000,
):
    if max_depth <= 0:
        return "[TRUNCATED_DEPTH]"
    if isinstance(payload, dict):
        output = {}
        for index, (key, value) in enumerate(payload.items()):
            if index >= max_items:
                output["__truncated__"] = True
                break
            if any(keyword in str(key).lower() for keyword in SENSITIVE_KEYWORDS):
                output[key] = REDACTED_VALUE
            else:
                output[key] = sanitize_for_trace(
                    value,
                    max_depth=max_depth - 1,
                    max_items=max_items,
                    max_string_length=max_string_length,
                )
        return output
    if isinstance(payload, list):
        items = []
        for index, value in enumerate(payload):
            if index >= max_items:
                items.append("[TRUNCATED_ITEMS]")
                break
            items.append(
                sanitize_for_trace(
                    value,
                    max_depth=max_depth - 1,
                    max_items=max_items,
                    max_string_length=max_string_length,
                )
            )
        return items
    if isinstance(payload, str) and len(payload) > max_string_length:
        return f"{payload[:max_string_length]}...[TRUNCATED]"
    return payload

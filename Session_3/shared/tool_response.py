"""Standard success/error envelopes for tool return values."""

from typing import Any


def success_response(data: dict, source: str = "local") -> dict:
    """Return a success envelope with optional source metadata."""
    envelope: dict[str, Any] = {
        "status": "success",
        "source": source,
        "safe_for_user": True,
    }
    envelope.update(data)
    return envelope


def error_response(
    error_type: str,
    message: str,
    safe_for_user: bool = True,
) -> dict:
    """Return an error envelope."""
    return {
        "status": "error",
        "error_type": error_type,
        "message": message,
        "safe_for_user": safe_for_user,
    }


if __name__ == "__main__":
    print(success_response({"priority": "high"}, source="local"))
    print(error_response("invalid_input", "Unsupported severity."))

"""Input validation helpers for tool boundaries."""


def validate_choice(
    value: str,
    allowed: list[str],
    field_name: str,
) -> tuple[bool, str | None]:
    """Return (True, None) if value is in allowed, else (False, message)."""
    if not isinstance(value, str):
        return False, f"{field_name} must be a string."

    normalized = value.strip().lower()
    if normalized not in allowed:
        options = ", ".join(allowed)
        return False, f"Unsupported {field_name}. Use one of: {options}."

    return True, None


def validate_positive_int(
    value: int,
    field_name: str,
) -> tuple[bool, str | None]:
    """Return (True, None) if value is a positive int, else (False, message)."""
    if isinstance(value, bool) or not isinstance(value, int):
        return False, f"{field_name} must be an integer."

    if value <= 0:
        return False, f"{field_name} must be a positive number (> 0)."

    return True, None


if __name__ == "__main__":
    print(validate_choice("HIGH", ["low", "medium", "high"], "severity"))
    print(validate_choice("urgent", ["low", "medium", "high"], "severity"))
    print(validate_positive_int(1, "product_id"))
    print(validate_positive_int(-5, "product_id"))

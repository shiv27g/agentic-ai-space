import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.logging_utils import log_tool_call
from shared.tool_response import error_response, success_response
from shared.validators import validate_choice

ISSUE_TYPES = ["billing", "technical", "access", "general"]
CUSTOMER_TIERS = ["premium", "standard"]
SEVERITIES = ["low", "medium", "high"]


def estimate_support_priority(
    issue_type: str,
    customer_tier: str,
    severity: str,
) -> dict:
    """Estimate support ticket priority from issue type, tier, and severity."""
    start = time.perf_counter()
    input_data = {
        "issue_type": issue_type,
        "customer_tier": customer_tier,
        "severity": severity,
    }

    for value, allowed, name in (
        (issue_type, ISSUE_TYPES, "issue_type"),
        (customer_tier, CUSTOMER_TIERS, "customer_tier"),
        (severity, SEVERITIES, "severity"),
    ):
        ok, message = validate_choice(value, allowed, name)
        if not ok:
            latency = (time.perf_counter() - start) * 1000
            log_tool_call(
                "estimate_support_priority",
                input_data,
                status="error",
                latency_ms=latency,
                error_type="invalid_input",
            )
            return error_response("invalid_input", message)

    issue = issue_type.strip().lower()
    tier = customer_tier.strip().lower()
    sev = severity.strip().lower()

    if sev == "high" and (tier == "premium" or issue == "billing"):
        priority = "high"
    elif sev == "high" or (sev == "medium" and tier == "premium"):
        priority = "medium"
    else:
        priority = "low"

    reason = (
        f"{tier.capitalize()} customer with {issue} issue "
        f"and {sev} severity."
    )

    latency = (time.perf_counter() - start) * 1000
    log_tool_call(
        "estimate_support_priority",
        input_data,
        status="success",
        latency_ms=latency,
    )
    return success_response(
        {"priority": priority, "reason": reason},
        source="local",
    )


def main() -> None:
    print(estimate_support_priority("billing", "premium", "high"))
    print(estimate_support_priority("general", "standard", "low"))
    print(estimate_support_priority("billing", "premium", "urgent"))


if __name__ == "__main__":
    main()

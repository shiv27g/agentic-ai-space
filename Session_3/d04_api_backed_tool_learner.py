"""API-backed tools: product lookup (DummyJSON) and currency rates (Frankfurter).

Both APIs are free, need no API key, and return real HTTP responses.

Run:
    python demos/d04_api_backed_tool_learner.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests

from shared.logging_utils import log_tool_call
from shared.tool_response import error_response, success_response
from shared.validators import validate_positive_int

PRODUCTS_API_BASE = "https://dummyjson.com/products"
EXCHANGE_API_BASE = "https://api.frankfurter.app/latest"
TIMEOUT_SECONDS = 5  # max time to wait for the API to respond


def _validate_currency_code(value: str, field_name: str) -> tuple[bool, str | None]:
    if not isinstance(value, str) or not value.strip(): # boundry check
        return False, f"{field_name} must be a non-empty string."

    code = value.strip().upper() 
    if len(code) != 3 or not code.isalpha():
        return False, f"{field_name} must be a 3-letter currency code (e.g. USD, INR)."

    return True, None


def get_product_details(product_id: int) -> dict:
    """Fetch normalized product details from DummyJSON.

    Args:
        product_id: A positive integer product id, e.g. 1.

    Returns:
        Success: {"status": "success", "source": "dummyjson_api", ...}
        Error:   normalized error envelope (invalid_input | not_found |
                  timeout | upstream_error).
    """
    start = time.perf_counter()
    input_data = {"product_id": product_id}

    ok, message = validate_positive_int(product_id, "product_id") # boundry check
    if not ok:
        latency = (time.perf_counter() - start) * 1000 # log the call - calculate latency
        log_tool_call(
            "get_product_details",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="invalid_input",
        )
        return error_response("invalid_input", message)

    url = f"{PRODUCTS_API_BASE}/{product_id}"

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
    except requests.Timeout:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_product_details",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="timeout",
        )
        return error_response(
            "timeout",
            "The product service took too long to respond. Please try again.",
        )
    except requests.RequestException:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_product_details",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="upstream_error",
        )
        return error_response(
            "upstream_error",
            "Could not reach the product service right now.",
        )

    if response.status_code == 404:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_product_details",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="not_found",
        )
        return error_response(
            "not_found",
            f"No product found with id {product_id}.",
        )
    if response.status_code != 200:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_product_details",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="upstream_error",
        )
        return error_response(
            "upstream_error",
            "The product service returned an unexpected response.",
        )

    try:
        raw = response.json() # check if the response is valid JSON
    except ValueError:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_product_details",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="upstream_error",
        )
        return error_response(
            "upstream_error",
            "The product service returned data we could not read.",
        )

    normalized = {
        "product_id": raw.get("id"),
        "title": raw.get("title"),
        "category": raw.get("category"),
        "price": raw.get("price"),
    }

    latency = (time.perf_counter() - start) * 1000
    log_tool_call(
        "get_product_details",
        input_data,
        status="success",
        latency_ms=latency,
    )
    return success_response(normalized, source="dummyjson_api")


def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """Fetch the latest exchange rate between two currencies (Frankfurter API).

    Args:
        from_currency: 3-letter code, e.g. "USD".
        to_currency: 3-letter code, e.g. "INR".

    Returns:
        Success: {"status": "success", "source": "frankfurter_api", ...}
        Error:   normalized error envelope (invalid_input | not_found |
                  timeout | upstream_error).
    """
    # https://api.frankfurter.dev/v1/latest?from=USD&to=INR
    start = time.perf_counter()
    input_data = {
        "from_currency": from_currency,
        "to_currency": to_currency,
    }

    for value, name in ((from_currency, "from_currency"), (to_currency, "to_currency")):
        ok, message = _validate_currency_code(value, name)
        if not ok:
            latency = (time.perf_counter() - start) * 1000
            log_tool_call(
                "get_exchange_rate",
                input_data,
                status="error",
                latency_ms=latency,
                error_type="invalid_input",
            )
            return error_response("invalid_input", message)

    from_code = from_currency.strip().upper()
    to_code = to_currency.strip().upper()
    url = f"{EXCHANGE_API_BASE}?from={from_code}&to={to_code}"

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
    except requests.Timeout:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_exchange_rate",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="timeout",
        )
        return error_response(
            "timeout",
            "The exchange rate service took too long to respond. Please try again.",
        )
    except requests.RequestException:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_exchange_rate",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="upstream_error",
        )
        return error_response(
            "upstream_error",
            "Could not reach the exchange rate service right now.",
        )

    if response.status_code == 404:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_exchange_rate",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="not_found",
        )
        return error_response(
            "not_found",
            f"No exchange rate available for {from_code} to {to_code}.",
        )
    if response.status_code != 200:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_exchange_rate",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="upstream_error",
        )
        return error_response(
            "upstream_error",
            "The exchange rate service returned an unexpected response.",
        )

    try:
        raw = response.json()
    except ValueError:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_exchange_rate",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="upstream_error",
        )
        return error_response(
            "upstream_error",
            "The exchange rate service returned data we could not read.",
        )

    rates = raw.get("rates") or {}
    rate = rates.get(to_code)
    if rate is None:
        latency = (time.perf_counter() - start) * 1000
        log_tool_call(
            "get_exchange_rate",
            input_data,
            status="error",
            latency_ms=latency,
            error_type="not_found",
        )
        return error_response(
            "not_found",
            f"No exchange rate available for {from_code} to {to_code}.",
        )

    normalized = {
        "from_currency": from_code,
        "to_currency": to_code,
        "rate": rate,
        "rate_date": raw.get("date"),
        "note": f"1 {from_code} equals {rate} {to_code} on the rate date.",
    }

    latency = (time.perf_counter() - start) * 1000
    log_tool_call(
        "get_exchange_rate",
        input_data,
        status="success",
        latency_ms=latency,
    )
    return success_response(normalized, source="frankfurter_api")


def main() -> None:
    print("=" * 60)
    print("DEMO 4 — API-backed tools")
    print("=" * 60)

    print("\n--- Product success: id 1 ---")
    print(get_product_details(1))

    print("\n--- Product error: invalid id (-5) ---")
    print(get_product_details(-5))

    print("\n--- Product error: not found (999999) ---")
    print(get_product_details(999999))

    print("\n--- Currency success: USD to INR ---")
    print(get_exchange_rate("USD", "INR"))

    print("\n--- Currency error: invalid code (US) ---")
    print(get_exchange_rate("US", "INR"))

    print("\n--- Currency error: unsupported code (USD to XXX) ---")
    print(get_exchange_rate("USD", "XXX"))


if __name__ == "__main__":
    main()

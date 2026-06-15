"""Structured stdout logging for tool calls."""

import json
import time
from typing import Any


def log_tool_call(
    tool_name: str,
    input_data: dict,
    status: str,
    latency_ms: float,
    error_type: str | None = None,
) -> None:
    """Print one JSON log line for a tool call."""
    log_line: dict[str, Any] = {
        "ts": round(time.time(), 3),
        "tool": tool_name,
        "status": status,
        "latency_ms": round(latency_ms, 2),
        "input": input_data,
    }
    if error_type is not None:
        log_line["error_type"] = error_type

    print("LOG " + json.dumps(log_line))


if __name__ == "__main__":
    start = time.perf_counter()
    time.sleep(0.01)
    elapsed = (time.perf_counter() - start) * 1000
    log_tool_call(
        tool_name="demo_tool",
        input_data={"x": 1},
        status="success",
        latency_ms=elapsed,
    )
    log_tool_call(
        tool_name="demo_tool",
        input_data={"x": -1},
        status="error",
        latency_ms=0.5,
        error_type="invalid_input",
    )

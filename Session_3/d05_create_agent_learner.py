"""Agent with reliable tools using LangChain create_agent (simpler than a manual loop).

Run:
    python demos/d05_create_agent_learner.py

Requires OPENAI_API_KEY in your environment (see .env.example).
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from dotenv import load_dotenv

load_dotenv()


from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

from Session_3_4.demo_3 import estimate_support_priority as _priority
from Session_3_4.d04_api_backed_tool_learner import (
    get_exchange_rate as _exchange_rate,
    get_product_details as _product,
)


@tool
def estimate_support_priority(
    issue_type: str, customer_tier: str, severity: str
) -> dict:
    """Estimate a support ticket priority.

    Args:
        issue_type: one of billing | technical | access | general
        customer_tier: one of premium | standard
        severity: one of low | medium | high

    Returns a normalized dict with status "success" or "error".
    """
    return _priority(issue_type, customer_tier, severity)


@tool
def get_product_details(product_id: int) -> dict:
    """Fetch normalized product details by positive integer id (e.g. 1).

    Returns a normalized dict with status "success" or "error".
    """
    return _product(product_id)


@tool
def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """Fetch the latest exchange rate between two 3-letter currency codes.

    Args:
        from_currency: e.g. "USD"
        to_currency: e.g. "INR"

    Returns a normalized dict with status "success" or "error".
    """
    return _exchange_rate(from_currency, to_currency)


TOOLS = [estimate_support_priority, get_product_details, get_exchange_rate]

SYSTEM_PROMPT = (
    "You are a helpful support assistant with access to reliable tools. "
    "Use tools when needed. Tool results include status 'success' or 'error' — "
    "explain outcomes clearly to the user, including safe error messages."
)


def run_prompt(agent, user_text: str) -> None:
    """Send one user message through the agent and print a readable trace."""
    print("\n" + "=" * 60)
    print(f"USER: {user_text}")
    print("=" * 60)

    result = agent.invoke({"messages": [HumanMessage(content=user_text)]})

    for msg in result["messages"]:
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for call in tool_calls:
                print(f"AGENT wants tool: {call['name']}({call['args']})")
        if isinstance(msg, ToolMessage):
            print(f"TOOL result: {msg.content}")

    final = result["messages"][-1]
    if getattr(final, "content", None):
        print(f"AGENT: {final.content}")


def main() -> None:
    print("=" * 60)
    print("DEMO 5b — Agent with reliable tools (create_agent)")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print(
            "\nOPENAI_API_KEY is not set.\n"
            "1) Copy .env.example to .env\n"
            "2) Put your key in OPENAI_API_KEY\n"
            "3) Re-run:  python demos/d05_create_agent_learner.py\n"
        )
        return

    agent = create_agent(
        model="gpt-4o-mini",
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )

    run_prompt(
        agent,
        "A premium customer has a high severity billing issue. "
        "What priority should we assign?",
    )
    run_prompt(agent, "Can you fetch details for product 1?")
    run_prompt(agent, "Can you fetch details for product -5?")
    run_prompt(agent, "What is the current USD to INR exchange rate?")
    run_prompt(
        agent,
        "A standard customer has an unsupported issue type called "
        "random_problem with low severity. What priority?",
    )


if __name__ == "__main__":
    main()

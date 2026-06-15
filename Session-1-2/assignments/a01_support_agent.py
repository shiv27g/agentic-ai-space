"""
SESSION 1 PROOF OF PROGRESS: Conversational Support Agent v1
============================================================
A production-aware support agent that combines everything from Day 1:
  - Configurable persona (SystemMessage)
  - chat() function with conversation memory
  - Error handling (specific exceptions, not a bare except)
  - Structured JSON logging with latency + token usage
  - A 4-turn simulated conversation + a token-cost summary

Anchor: A demo gives a response. A system gives a trace.

Run:  python assignments/a01_support_agent.py

Reflection to submit (5 lines):
  1. What did I build?
  2. Where is memory handled?
  3. Where can this fail?
  4. What did I add to make it production-aware?
  5. What will I improve next?
"""

import json
import logging
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ---------- logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("support_agent")

# ---------- configurable persona ----------
COMPANY = "TechShop"
PERSONA = (
    f"You are a customer support agent for {COMPANY}, an electronics store. "
    "Be helpful, professional, and concise. Answer in 2-3 sentences max."
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# conversation memory (owned by THIS application)
conversation = [SystemMessage(content=PERSONA)]

# running totals for the cost summary
totals = {"input_tokens": 0, "output_tokens": 0, "turns": 0}


def chat(user_input: str, session_id: str = "sess-001") -> str:
    """One support turn: append input, call LLM with logging + error handling, store reply."""
    start = time.time()
    conversation.append(HumanMessage(content=user_input))

    try:
        response = llm.invoke(conversation)
    except ValueError as e:
        logger.error(json.dumps({"event": "llm_error", "type": "ValueError", "msg": str(e)}))
        return "Sorry, that input couldn't be processed."
    except TimeoutError as e:
        logger.error(json.dumps({"event": "llm_error", "type": "Timeout", "msg": str(e)}))
        return "The request timed out. Please try again."
    except Exception as e:  # last-resort fallback — the user never sees a stack trace
        logger.error(json.dumps({"event": "llm_error", "type": type(e).__name__, "msg": str(e)}))
        return "Something went wrong. Our team has been notified."

    if not response.content or not response.content.strip():
        logger.warning(json.dumps({"event": "empty_response", "session_id": session_id}))
        return "I couldn't generate a response. Please try again."

    conversation.append(response)  # store the agent's reply -> memory continuity

    latency_ms = round((time.time() - start) * 1000, 2)
    usage = response.usage_metadata or {}
    totals["input_tokens"] += usage.get("input_tokens", 0)
    totals["output_tokens"] += usage.get("output_tokens", 0)
    totals["turns"] += 1

    logger.info(json.dumps({
        "event": "turn_success",
        "session_id": session_id,
        "turn": totals["turns"],
        "latency_ms": latency_ms,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
    }))
    return response.content


def main() -> None:
    print("=" * 60)
    print(f"{COMPANY} Support Agent v1")
    print("=" * 60)

    for user_msg in [
        "Hi, what is your return policy?",
        "How long is the return window?",
        "I bought a laptop 25 days ago — can I still return it?",
        "Great. How do I start the return?",
    ]:
        reply = chat(user_msg)
        print(f"\nUser:  {user_msg}")
        print(f"Agent: {reply}")

    print("\n" + "=" * 60)
    print("TOKEN / COST SUMMARY")
    print(json.dumps(totals, indent=2))
    print("A system gives a trace — you can now answer: how many tokens did this session cost?")


if __name__ == "__main__":
    main()

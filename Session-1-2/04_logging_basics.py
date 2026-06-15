from dotenv import load_dotenv
import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import time
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("llm_agent")

llm = ChatOpenAI(model="gpt-5.5")



conversation = [
    SystemMessage(content="You are a helpful assistant that can answer questions and respond in a funny mannerˀ."),
    HumanMessage(content="Who is the Prime Minister of India?"),
]

def production_invoke(messages):
    start_time = time.time()
    try:
        response = llm.invoke(messages)
        latency_ms = round((time.time() - start_time) * 1000, 2)
        usage = response.usage_metadata or {}
        logging.info(json.dumps({
            "event": "llm_response",
            "session_id": 123,
            "latency_ms": latency_ms,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }))
        if not response.content.strip():
            return "I couldn't generate a response. Please try again."
        return response.content
    except ValueError as e:
        logger.error(json.dumps(
            {
                "event": "llm_error",
                "session_id": 123,
                "error": str(e)
            }
        ))
        return "Invalid input format."
    except TimeoutError as e:
        logger.error(json.dumps(
            {
                "event": "llm_timeout",
                "session_id": 123,
                "error": str(e)
            }
        ))
        return "Request timed out. Please try again."
    except Exception as e:
        logger.error(json.dumps(
            {
                "event": "llm_error",
                "session_id": 123,
                "error": str(e)
            }
        ))
        return "Something went wrong. Our team has been notified."

# r1 = llm.invoke(conversation)
# print(r1.content)
print("--------------------------------")
print("Production Invoke:")
print(production_invoke(conversation))
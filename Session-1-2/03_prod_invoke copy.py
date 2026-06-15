from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
load_dotenv()

llm = ChatOpenAI(model="gpt-5.5")

conversation = [
    SystemMessage(content="You are a helpful assistant that can answer questions and respond in a funny mannerˀ."),
    HumanMessage(content="Who is the Prime Minister of India?"),
]

def production_invoke(messages):
    try:
        response = llm.invoke(messages)
        if not response.content.strip():
            return "I couldn't generate a response. Please try again."
        return response.content
    except ValueError as e:
        return "Invalid input format."
    except TimeoutError as e:
        return "Request timed out. Please try again."
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return "Something went wrong. Our team has been notified."

# r1 = llm.invoke(conversation)
# print(r1.content)
print("--------------------------------")
print("Production Invoke:")
print(production_invoke(conversation))
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()

def get_weather(city: str) -> str:
    """
    Get the current weather for a given city
    Use this when the user asks about weather, temperature or climate.
    
    Args:
        city: the name of the city (e.g. 'Mumbai', 'Delhi', 'London')
    Returns:
        The current weather for the given city
    """
    weather_data = {
        'mumbai': 'sunny',
        'delhi': 'cloudy',
        'london': 'rainy',
    }
    weather = weather_data.get(city.lower(), 'unknown')
    return f"The weather in {city} is {weather}"

@tool
def book_flight(origin: str, destination: str, date: str) -> dict:
    """Book a flight between two cities. Use when the user wants to book travel.

    Args:
        origin: departure city
        destination: arrival city
        date: travel date (YYYY-MM-DD)
    """
    return {"booking_id": "FL12345", "route": f"{origin} -> {destination}",
            "date": date, "status": "confirmed"}

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather, book_flight],
    system_prompt="You are a helpful assistant that can book flights and check weather.",
)
r1 = agent.invoke({"messages": [{"role": "user",
              "content": "what is the weather in mumbai"}]}) # documentation approach
print(r1)
print("--------------------------------")
r2 = agent.invoke({"messages": [HumanMessage(content="what is the weather in delhi")]}) # direct approach
print(r2)
print("--------------------------------")
r3 = agent.invoke({"messages": [HumanMessage(content="Who is the Author of the book 'The Great Gatsby'?")]}) # direct approach
print(r3)
print("--------------------------------")
r4 = agent.invoke({"messages": [HumanMessage(content="Book a flight from Mumbai to Delhi on 2026-06-08")]}) # direct approach
print(r4)
print("--------------------------------")
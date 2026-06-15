from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class SupportState(TypedDict): # STATE
    query: str
    issue_category: str
    response: str

# Node
def classify(state: SupportState) -> SupportState:
    if "billing" in state['query'].lower():
        return {'issue_category': 'billing'}
    elif "technical" in state['query'].lower():
        return {'issue_category': 'technical'}
    else:
        return {'issue_category': 'general'}

def respond(state: SupportState) -> SupportState:
    if state['issue_category'] == 'billing':
        return {'response': 'Please wait while we investigate the billing issue.'}
    elif state['issue_category'] == 'technical':
        return {'response': 'Please wait while we investigate the technical issue.'}
    else:
        return {'response': 'Please wait while we investigate the issue.'}

graph = StateGraph(SupportState)
graph.add_node("classify", classify)
graph.add_node("respond", respond)
graph.add_edge(START, "classify")
graph.add_edge("classify", "respond")
graph.add_edge("respond", END)


app = graph.compile()
# export to png
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

display(Image(app.get_graph().draw_mermaid_png()))

response = app.invoke({"query": "I have a billing issue"}) # billing
print(response)
print("--------------------------------")
response = app.invoke({"query": "I have a technical issue"}) # technical
print(response)
print("--------------------------------")
response = app.invoke({"query": "I have a authorization issue"}) # general
print(response)
print("--------------------------------")
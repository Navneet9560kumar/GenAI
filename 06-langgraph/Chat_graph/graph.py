from dotenv import load_dotenv
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

load_dotenv()

class State(TypedDict):
    messages: list

llm = init_chat_model(model_provider="openai", model="gpt-4")

def chat_node(state: State):
    responce = llm.invoke(state["messages"])
    return {"messages": [responce]}

graph_builder = StateGraph(State)

graph_builder.add_node("chat_node", chat_node)

graph_builder.add_edge(START, "chat_node")

# ✅ Add this line to connect the flow to END
graph_builder.add_edge("chat_node", END)

graph = graph_builder.compile()

def main():
    query = input(">")
    result = graph.invoke({"messages": [{"role": "user", "content": query}]})
    print(result)

if __name__ == "__main__":
    main()

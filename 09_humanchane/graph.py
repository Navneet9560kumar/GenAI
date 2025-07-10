from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode  # ✅ Corrected: preduilt → prebuilt
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END  # ✅ Corrected: langchain.graph → langgraph.graph

tools = []

class State(TypedDict):
    messages: Annotated[list, add_messages]  # ✅ Fixed: missing field name

# ✅ Moved model initialization outside class
llm = init_chat_model(model_provider="openai", model="gpt-4.1")
llm_with_tools = llm.bind_tools(tools=tools)  # ✅ Fixed: wrong keyword 'tool' → 'tools'

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])  # ✅ Fixed: key should be "messages"
    return {"messages": [message]}  # ✅ Fixed: retrun → return

tools_nodes = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tools_nodes)

graph_builder.add_edge("START", "chatbot") 
graph_builder.add_conditional_edges("chatbot", tools_conditions)

graph_builder.add_edge("chatbot", "chatbot") 
graph_builder.add_edge("chatbot", "END")

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


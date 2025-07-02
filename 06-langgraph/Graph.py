from typing import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
from typing_extensions import TypeAlias
from langgraph.graph import StateGraph, START, END

# Load environment variables (for OpenAI API key)
load_dotenv()

client = OpenAI()  # This uses OPENAI_API_KEY from .env

# Define the state structure
class State(TypedDict):
    query: str
    llm_result: str | None

# Node function to process the query
def chat_bot(state: State) -> State:
    query = state['query']
    llm_response = client.chat.completions.create(
        model="gpt-4o",  # Or use "gpt-3.5-turbo" if not on Pro
        messages=[
            {
                "role": "user",
                "content": query
            }
        ]
    )
    result = llm_response.choices[0].message.content
    state["llm_result"] = result
    return state

# Define the state graph
graph_builder = StateGraph(State)

# Add a node and transitions
graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

# Compile the graph
graph = graph_builder.compile()

# Main function to run the graph
def main():
    user = input("👤 You: ")
    state = {
        "query": user,
        "llm_result": None
    }
    result = graph.invoke(state)
    print("🤖 Bot:", result["llm_result"])

if __name__ == "__main__":
    main()

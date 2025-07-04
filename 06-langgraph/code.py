from typing_extensions import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
from typing import Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
import json

load_dotenv()
client = OpenAI()


class ClassifyMessageResponse(BaseModel):
    is_Coding_question: bool


class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: str


class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_Coding_question: bool | None


def classify_message(state: State):
    query = state['user_query']
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user query is a coding question or not.
    Return the response in JSON format like: {"is_Coding_question": true}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    content = response.choices[0].message.content
    try:
        parsed = json.loads(content)
        state["is_Coding_question"] = parsed.get("is_Coding_question", False)
    except json.JSONDecodeError:
        state["is_Coding_question"] = False

    return state


def rought_query(state: State) -> Literal["genral_query", "coding_query"]:
    is_coding = state["is_Coding_question"]
    if is_coding:
        return "coding_query"
    return "genral_query"


def general_query(state: State):
    query = state["user_query"]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    state["llm_result"] = response.choices[0].message.content
    return state


def coding_query(state: State):
    query = state["user_query"]
    SYSTEM_PROMPT = "You are a coding assistant."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    state["llm_result"] = response.choices[0].message.content
    return state


def coding_validate_query(state: State):
    query = state["user_query"]
    SYSTEM_PROMPT = f"""
    You are an expert in calculating the accuracy of code according to the user query.
    Return the percentage of accuracy in JSON format like: {{"accuracy_percentage": "90%"}}

    User Query: {query}
    Code: {state["llm_result"]}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    content = response.choices[0].message.content
    try:
        parsed = json.loads(content)
        state["accuracy_percentage"] = parsed.get("accuracy_percentage", "Unknown")
    except json.JSONDecodeError:
        state["accuracy_percentage"] = "Unknown"
    return state


# === GRAPH ===
graph_builder = StateGraph(State)

graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("rought_query", rought_query)
graph_builder.add_node("genral_query", general_query)
graph_builder.add_node("coding_query", coding_query)
graph_builder.add_node("coding_validate_query", coding_validate_query)

graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", rought_query, {
    "genral_query": "genral_query",
    "coding_query": "coding_query"
})
graph_builder.add_edge("genral_query", END)
graph_builder.add_edge("coding_query", "coding_validate_query")
graph_builder.add_edge("coding_validate_query", END)

graph = graph_builder.compile()

# === MAIN ===
def main():
    user = input("You: ")
    state = {
        "user_query": user,
        "accuracy_percentage": None,
        "is_Coding_question": None,
        "llm_result": None
    }

def main():
    user = input("You: ")
    state = {
        "user_query": user,
        "accuracy_percentage": None,
        "is_Coding_question": None,
        "llm_result": None
    }

    for event in graph.stream(state):
        print("Event:", event)

# Run main function
if __name__ == "__main__":
    main()

#     result = graph.invoke(state)
#     print("\n🤖 Response:", result["llm_result"])
#     if result.get("accuracy_percentage"):
#         print("✅ Code Accuracy:", result["accuracy_percentage"])
#     main()

# if __name__ == "__main__":
#     main()

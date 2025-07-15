from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json
from neo4j import GraphDatabase  # 👉 Neo4j manual insert support

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=OPEN_API_KEY)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPEN_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPEN_API_KEY,
            "model": "gpt-4.1"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": "6333"
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://cafdc5b3.databases.neo4j.io",
            "username": "neo4j",
            "password": "rBepG9CZp2FfS72JfuW6srwYJ2G_ALsptdmOQFDHT1E"
        }
    }
}

mem_client = Memory.from_config(config)

# 👉 Neo4j config and function to insert user-query-response into graph
uri = config["graph_store"]["config"]["url"]
username = config["graph_store"]["config"]["username"]
password = config["graph_store"]["config"]["password"]
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_memory(tx, user, question, response):
    tx.run(
        """
        MERGE (u:User {name: $user})
        CREATE (q:Query {text: $question})
        CREATE (a:Answer {text: $response})
        CREATE (u)-[:ASKED]->(q)
        CREATE (q)-[:ANSWERED_WITH]->(a)
        """,
        user=user,
        question=question,
        response=response
    )

def insert_into_graph(user, question, response):
    with driver.session() as session:
        session.write_transaction(create_memory, user, question, response)

def chat():
    while True:
        user_query = input("> ")
        relevent_memories = mem_client.search(query=user_query, user_id="Navneet")
        memories = [
            f"ID:{men.get('id')}, Memory: {men.get('memory')}" for men in relevent_memories.get("results")
        ]
        SYSTEM_PROMPT = f"""
You are a memory-aware assistant which responds to the user with context.
You are given past memories and facts about the user.

Memory of the user:
{json.dumps(memories)}
"""
        result = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        )
        response_text = result.choices[0].message.content
        print(f"😎 : {response_text}")

        mem_client.add([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response_text},
        ], user_id="Navneet")

        # 👉 Store this conversation into Neo4j graph
        insert_into_graph("Navneet", user_query, response_text)

if __name__ == "__main__":
    chat()

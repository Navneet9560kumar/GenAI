from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json

# ✅ Load environment variables
load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

# ✅ OpenAI client
client = OpenAI(api_key=OPEN_API_KEY)

# ✅ Config for mem0 with Qdrant
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
    }
}

# ✅ Create Memory client
mem_client = Memory.from_config(config)

# ✅ Chat loop
def chat():
    while True:
        user_query = input("> ")

        # 🔍 Search previous memories
        relevent_memories = mem_client.search(query=user_query, user_id="Navneet")

        # 🧠 Extract memory entries
        memories = [
            f"ID:{men.get('id')}, Memory: {men.get('memory')}" for men in relevent_memories.get("results")
        ]

        # 📝 Create system prompt with memory context
        SYSTEM_PROMPT = f"""
You are a memory-aware assistant which responds to the user with context.
You are given past memories and facts about the user.

Memory of the user:
{json.dumps(memories)}
"""

        # 🤖 Generate assistant response
        result = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        )

        # 📤 Print assistant response
        print(f"😎 : {result.choices[0].message.content}")

        # 💾 Store interaction in memory
        mem_client.add([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": result.choices[0].message.content},
        ], user_id="Navneet")

# 🚀 Start the chat
if __name__ == "__main__":
    chat()

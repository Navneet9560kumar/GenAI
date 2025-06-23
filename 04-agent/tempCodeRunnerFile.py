from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

client = OpenAI()

SYSTEM_PROMPT= """

You are a helpful AI Assistant
"""

response = client.chat.completions.create(
      model="gpt-4.1",
      messages=[
            {"role":"user","content":"What is date and time today"}
      ]
)

print("The Response ", response.choices[0].message.content)
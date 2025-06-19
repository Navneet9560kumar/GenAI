from dotenv import load_dotenv
import os
from openai import OpenAI

# Load .env variables
load_dotenv()

# Initialize client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

text = "dog chases cat"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print(response)
 
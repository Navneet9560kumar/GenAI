from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client for chat
client = OpenAI()

# Vector Embedding
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Load vector DB
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

# Take a user Query
query = input("> ")

# Vector Similarity Search [query] in DB
search_results = vector_db.similarity_search(query=query)

print("search_result", search_results)

context = "\n\n".join([
    f"Page Content: {result.page_content} \nPage Number: {result.metadata.get('page_label', 'N/A')}\n"
    for result in search_results
])

# Final Prompt
SYSTEM_PROMPT = """
YOU are a helpful AI Assistant who answers user queries based on the available context retrieved from a PDF file, including page contents and page numbers.

You should only answer the user based on the following context and guide them to open the correct page number to learn more.
"""

FINAL_PROMPT = f"""{SYSTEM_PROMPT}
Context:
{context}
"""

# ✅ Now this will work correctly
chat_completion = client.chat.completions.create(
    model="gpt-4-1106-preview",  # or "gpt-3.5-turbo" if you don't have GPT-4 access
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
)

print(f"🤖🤖: {chat_completion.choices[0].message.content}")


 #tasis a 🤖🤖🤖🤖 =  Blog likhana hai & byy using a Streamlit make a RAG
 #1=> heading  is a RAg chat application 2=> user ke pass input button    or fir ek butten aayega ready for chat fir baad mai  
 #button se pdf app uplode karege fir us se question puchege fir baad mai vo answer dega  

 # Arrtical = indexing , chuncking , 

 # challange web per bahut sara content hota hia to kay RAG per ek chatbot bana sakte hai ham 
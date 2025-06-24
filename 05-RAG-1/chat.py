from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import  QdrantVectorStore

load_dotenv()
# Vector Embedding

embedding_model = OpenAIEmbeddings(
      model="text-embedding-3-large"
)


vectro_db = QdrantVectorStore.from_existing_collection(
      url="http://localhost:6333",
        collection_name= "learing_vectros",
         embedding=embedding_model
)

# Take a user Query
query = input("> ")

#Vector Similary Search [query] in DB

search_results = vectro_db.similarity_search(
      query=query
)

print("search_result", search_results)


SYSTEM_PROMPT= F"""
            YOU are 

"""
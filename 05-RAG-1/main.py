from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
pdf_path = Path(__file__).parent / "nodejs.pdf"

from langchain_openai import OpenAIEmbeddings

from langchain_qdrant import  QdrantVectorStore
#Loding
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()

load_dotenv()

print("Docs[0]", docs[5])


# chunking = matlb ye ke divied karna or sba karna 
text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap=400
)

split_docs = text_splitter.split_documents(documents=docs)

# Vector Embedding

embedding_model = OpenAIEmbeddings(
      model="text-embedding-3-large"
)


#  Using embedding_model create emmbedding of split_docs and store in DB

# so in  arket there have a lots of vectro embding  like a pinecode {(cloud and paid)}
#Astra DB, Chroma DB(Open Source), Milvus DB(OPenS),, QDrant DB(OS)
#why QDrant DB =  lightweight, spin up time is fast , OOTB UI, Namespacen


vector_store = QdrantVectorStore.from_documents(
      documents=split_docs,
      url="http://localhost:6333",
      collection_name= "learing_vectros",
      embedding=embedding_model
)

print("Indexing of Done....")
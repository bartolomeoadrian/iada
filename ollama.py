import logging
import sys
import chromadb
import os
from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

# log
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# llm
Settings.llm = Ollama(model="llama2", request_timeout=60.0)

# data
documents = SimpleDirectoryReader("data").load_data()

# vector store
db = chromadb.PersistentClient(path="./chroma")
chroma_collection = db.get_or_create_collection("ollama")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# embedding
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# query
query_engine = index.as_query_engine(llm=Ollama(model="llama2", request_timeout=60.0))
response = query_engine.query("De que trata la noticia?")
print(response)

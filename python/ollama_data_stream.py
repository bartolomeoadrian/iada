import logging
import sys
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

# log
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# llm
Settings.llm = Ollama(model="llama2", request_timeout=60.0)

# data
documents = SimpleDirectoryReader("data/txt").load_data()

# vector store
db = chromadb.PersistentClient(path="./chroma")
chroma_collection = db.get_or_create_collection("ollama")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# embedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)

# query
query_engine = index.as_query_engine(
    streaming=True, llm=Ollama(model="llama2", request_timeout=120.0)
)
response_stream = query_engine.query("De que trata la noticia?")
response_stream.print_response_stream()

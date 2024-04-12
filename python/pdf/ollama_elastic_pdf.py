import logging
import sys
import chromadb
import documents
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


# log
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# llm
Settings.llm = Ollama(model="tinyllama", request_timeout=60.0)

# embedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# vector store
vector_store = ElasticsearchStore(
    index_name="pdf", es_url="http://localhost:9200"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context, show_progress=True
)

# query
query_engine = index.as_query_engine(
    streaming=True, llm=Ollama(model="tinyllama", request_timeout=120.0)
)
# response_stream = query_engine.query("De que trata el expediente 0774-D-88?\nRespond in Spanish\nSobre la república Argentina")
# response_stream.print_response_stream()

while True:
    query = input("Query: ")
    response_stream = query_engine.query(query + "\nRespond in Spanish\n")
    response_stream.print_response_stream()
    print("------")

import logging
import sys
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

# log
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# data
documents = SimpleDirectoryReader("data/txt").load_data()

# vector store
vector_store = ElasticsearchStore(
    index_name="txt", es_url="http://localhost:9200"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# embedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)

# query
query_engine = index.as_query_engine(
    streaming=True, llm=Ollama(model="mistral", request_timeout=120.0)
)
response_stream = query_engine.query("De que trata la noticia?\nRespond in Spanish\n")
response_stream.print_response_stream()

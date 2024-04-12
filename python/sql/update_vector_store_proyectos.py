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


Settings.chunk_size = 2048

# log
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# embedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# data
proyectos = documents.get_documents()

# vector store
vector_store = ElasticsearchStore(
    index_name="proyectos", es_url="http://localhost:9200"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    proyectos, storage_context=storage_context, show_progress=True
)

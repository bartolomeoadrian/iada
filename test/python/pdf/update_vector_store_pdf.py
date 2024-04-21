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
from llama_index.readers.smart_pdf_loader import SmartPDFLoader


Settings.chunk_size = 2048

# log
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# embedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# data
llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
pdf_url = "./data/pdf/mis_dias.pdf"  # also allowed is a file path e.g. /home/downloads/xyz.pdf
pdf_loader = SmartPDFLoader(llmsherpa_api_url=llmsherpa_api_url)
pdf = pdf_loader.load_data(pdf_url)

# vector store
vector_store = ElasticsearchStore(index_name="pdf", es_url="http://localhost:9200")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    pdf, storage_context=storage_context, show_progress=True
)

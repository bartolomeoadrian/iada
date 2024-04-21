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
llm = Ollama(model="llama2", request_timeout=120.0)

while True:
    query = input("Query: ")
    response = llm.complete(
        query + "\nRespond in Spanish\nSobre la república Argentina"
    )
    print(response)
    print("------")

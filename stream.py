import logging
import sys
import chromadb
from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import get_response_synthesizer

# log
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# llm
llm = Ollama(model="llama2", request_timeout=60.0)
response_stream  = llm.stream_complete("Hola! Como estas?")
response_stream = list(response_stream)
for response in response_stream:
	print(response)

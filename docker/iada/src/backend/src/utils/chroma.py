import os
import chromadb

chroma_url = os.environ.get("CHROMA_URL") or "http://localhost:8000"

print("""Connecting to ChromaDB at {}""".format(chroma_url))

chroma_client = chromadb.HttpClient(
    host=chroma_url.split("://")[1].split(":")[0],
    port=chroma_url.split("://")[1].split(":")[1],
)

import os
from .chroma import chroma_client
from vanna.chromadb import ChromaDB_VectorStore
from vanna.google import GoogleGeminiChat


class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(
            self,
            config={
                "api_key": os.environ["GEMINI_API_KEY"],
                "model": "gemini-1.5-flash",
            },
        )


vn = MyVanna(config={"client": chroma_client})

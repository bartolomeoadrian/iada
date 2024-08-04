from ..utils.chroma import chroma_client

collections = chroma_client.list_collections()
print(collections)

chroma_client.delete_collection("ddl")
chroma_client.delete_collection("documentation")

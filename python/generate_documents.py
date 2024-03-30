import json
from llama_index.core import Document
from llama_index.core.schema import MetadataMode

llama_documents = []

for document in documents_list:

    # Value for metadata must be one of (str, int, float, None)
    document["writers"] = json.dumps(document["writers"])
    document["languages"] = json.dumps(document["languages"])
    document["genres"] = json.dumps(document["genres"])
    document["cast"] = json.dumps(document["cast"])
    document["directors"] = json.dumps(document["directors"])
    document["countries"] = json.dumps(document["countries"])
    document["imdb"] = json.dumps(document["imdb"])
    document["awards"] = json.dumps(document["awards"])

    # Create a Document object with the text and excluded metadata for llm and embedding models
    llama_document = Document(
        text=document["fullplot"],
        metadata=document,
        excluded_llm_metadata_keys=["fullplot", "metacritic"],
        excluded_embed_metadata_keys=[
            "fullplot",
            "metacritic",
            "poster",
            "num_mflix_comments",
            "runtime",
            "rated",
        ],
        metadata_template="{key}=>{value}",
        text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
    )

    llama_documents.append(llama_document)

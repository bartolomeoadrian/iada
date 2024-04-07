import json
from llama_index.core import Document
from llama_index.core.schema import MetadataMode


def get_documents():
    f = open("./data/proyectos/8389_small.json", "r")
    documents_list = json.load(f)

    llama_documents = []

    for document in documents_list:
        # Create a Document object with the text and excluded metadata for llm and embedding models
        llama_document = Document(
            text=document["titulo"],
            metadata={
                "titulo del expediente": document["titulo"],
                "sumario del expediente": document["sumario"],
                "iniciado en": document["iniciado"],
                "expediente diputados": document["exp_dip"],
                "firmantes del expediente": document["firmantes"],
                # "ses_ing": document["ses_ing"],
                # "public": document["public"],
                # "tipo_doc": document["tipo_doc"],
                # "com_dip": document["com_dip"],
                "palabras clave del expediente": document["palabras_clave"],
            },
            # excluded_llm_metadata_keys=["fullplot", "metacritic"],
            # excluded_embed_metadata_keys=[
            #     "fullplot",
            #     "metacritic",
            #     "poster",
            #     "num_mflix_comments",
            #     "runtime",
            #     "rated",
            # ],
            metadata_template="{key}=>{value}",
            text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
        )

        llama_documents.append(llama_document)

    return llama_documents

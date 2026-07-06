from langchain_chroma import Chroma

from services.embeddings import get_embeddings


def get_vector_store():

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name="meeting_documents",
        embedding_function=embeddings,
        persist_directory="vector_db",
    )

    return vector_store
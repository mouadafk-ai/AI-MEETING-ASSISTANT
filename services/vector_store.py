from langchain_chroma import Chroma
from config import COLLECTION_NAME, VECTOR_DB_PATH

from services.embeddings import get_embeddings


def get_vector_store():

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )

    return vector_store
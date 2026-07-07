from pathlib import Path

from services.pdf_reader import read_pdf
from services.chunker import create_chunks
from services.vector_store import get_vector_store


def index_pdf(pdf_path: Path):
    text = read_pdf(pdf_path)
    chunks = create_chunks(text)

    vector_store = get_vector_store()

    # Verwijder oude chunks van hetzelfde bestand,
    # zodat oude versies geen verkeerde antwoorden geven.
    try:
        vector_store._collection.delete(where={"source": pdf_path.name})
    except Exception:
        pass

    metadatas = [
        {
            "source": pdf_path.name,
            "chunk": i,
        }
        for i in range(len(chunks))
    ]

    ids = [
        f"{pdf_path.name}-chunk-{i}"
        for i in range(len(chunks))
    ]

    vector_store.add_texts(
        texts=chunks,
        metadatas=metadatas,
        ids=ids,
    )

    return len(chunks)
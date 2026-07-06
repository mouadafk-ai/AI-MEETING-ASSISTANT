from datetime import datetime
from uuid import uuid4

from services.loader import save_uploaded_file
from services.pdf_reader import read_pdf
from services.indexer import index_pdf
from services.document_registry import DocumentRegistry


class DocumentManager:
    def __init__(self):
        self.registry = DocumentRegistry()

    def process_document(self, uploaded_file):
        file_path = save_uploaded_file(uploaded_file)
        pdf_text = read_pdf(file_path)
        chunk_count = index_pdf(file_path)

        document = {
            "id": str(uuid4())[:8],
            "name": uploaded_file.name,
            "chunks": chunk_count,
            "uploaded_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.registry.add(document)

        return {
            "file_path": file_path,
            "pdf_text": pdf_text,
            "chunk_count": chunk_count,
            "document": document,
        }
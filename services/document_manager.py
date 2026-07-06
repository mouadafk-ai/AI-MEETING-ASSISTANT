from pathlib import Path

from services.loader import save_uploaded_file
from services.pdf_reader import read_pdf
from services.indexer import index_pdf


class DocumentManager:

    def process_document(self, uploaded_file):
        """
        Slaat een PDF op, leest deze uit en indexeert hem.
        """

        file_path = save_uploaded_file(uploaded_file)

        pdf_text = read_pdf(file_path)

        chunk_count = index_pdf(file_path)

        return {
            "file_path": file_path,
            "pdf_text": pdf_text,
            "chunk_count": chunk_count,
        }
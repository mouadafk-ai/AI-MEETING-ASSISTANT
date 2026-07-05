from pathlib import Path
from pypdf import PdfReader


def read_pdf(pdf_path: Path) -> str:
 

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text
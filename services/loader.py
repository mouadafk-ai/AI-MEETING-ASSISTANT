from pathlib import Path
import streamlit as st


PDF_FOLDER = Path("data/pdfs")


def save_uploaded_file(uploaded_file):

    PDF_FOLDER.mkdir(parents=True, exist_ok=True)

    file_path = PDF_FOLDER / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
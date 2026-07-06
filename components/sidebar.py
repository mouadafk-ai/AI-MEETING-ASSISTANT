import streamlit as st

from services.document_manager import DocumentManager


document_manager = DocumentManager()


def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Instellingen")

        uploaded_file = st.file_uploader(
            "Upload een PDF",
            type=["pdf"],
        )

        if uploaded_file is not None:
            st.info(f"Geselecteerd bestand: {uploaded_file.name}")

            if st.button("📥 PDF opslaan en indexeren"):
                result = document_manager.process_document(uploaded_file)

                file_path = result["file_path"]
                pdf_text = result["pdf_text"]
                chunk_count = result["chunk_count"]

                st.session_state.pdf_indexed = True
                st.session_state.pdf_name = uploaded_file.name

                st.success("PDF opgeslagen en geïndexeerd.")
                st.info(f"Bestand: {file_path.name}")
                st.info(f"Aantal chunks: {chunk_count}")

                st.text_area(
                    "Uitgelezen tekst",
                    pdf_text,
                    height=300,
                )

        st.divider()

        if st.session_state.pdf_indexed:
            st.success(f"Actief document: {st.session_state.pdf_name}")
        else:
            st.warning("Nog geen PDF geïndexeerd.")

        st.divider()

        if st.button("🗑️ Nieuw gesprek"):
            st.session_state.chat_history = []
            st.session_state.conversation_id += 1
            st.rerun()
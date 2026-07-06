import streamlit as st

from services.document_manager import DocumentManager
from services.rag import ask_question

document_manager = DocumentManager()

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🤖",
    layout="wide",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_indexed" not in st.session_state:
    st.session_state.pdf_indexed = False

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

st.title("🤖 AI Meeting Assistant")
st.write("Upload een PDF, indexeer het document en stel daarna vragen over de inhoud.")

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

tab_chat, tab_summary, tab_actions = st.tabs(
    ["💬 Chat", "📝 Samenvatting", "✅ Actiepunten"]
)

with tab_chat:
    st.subheader("💬 Stel een vraag over je document")

    user_question = st.text_area(
        "Jouw vraag",
        placeholder="Bijvoorbeeld: Waar gaat dit document over?",
        height=120,
    )

    if st.button("Vraag stellen", type="primary"):
        if not st.session_state.pdf_indexed:
            st.error("Upload en indexeer eerst een PDF.")
        elif not user_question:
            st.error("Typ eerst een vraag.")
        else:
            with st.spinner("AI zoekt in je document..."):
                result = ask_question(user_question)

            st.session_state.chat_history.append(
                {
                    "question": user_question,
                    "answer": result["answer"],
                    "sources": result["sources"],
                }
            )

    st.divider()

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

            if chat.get("sources"):
                with st.expander("📚 Bronnen"):
                    for source in chat["sources"]:
                        st.write(
                            f"📄 {source['source']} (chunk {source['chunk']})"
                        )

with tab_summary:
    st.subheader("📝 Document samenvatten")

    if st.button("Maak samenvatting"):
        if not st.session_state.pdf_indexed:
            st.error("Upload en indexeer eerst een PDF.")
        else:
            st.info("Samenvatting bouwen we in de volgende stap.")

with tab_actions:
    st.subheader("✅ Actiepunten herkennen")

    if st.button("Haal actiepunten op"):
        if not st.session_state.pdf_indexed:
            st.error("Upload en indexeer eerst een PDF.")
        else:
            st.info("Actiepunten bouwen we daarna.")
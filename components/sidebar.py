import streamlit as st

from services.document_manager import DocumentManager
from services.conversation_manager import ConversationManager


document_manager = DocumentManager()
conversation_manager = ConversationManager()


def load_conversation(conversation):
    st.session_state.conversation_id = conversation["id"]

    messages = conversation.get("messages", [])
    chat_history = []
    pending_question = None

    for message in messages:
        if message["role"] == "user":
            pending_question = message["content"]

        elif message["role"] == "assistant" and pending_question:
            chat_history.append(
                {
                    "question": pending_question,
                    "answer": message["content"],
                    "sources": message.get("sources", []),
                }
            )
            pending_question = None

    documents = conversation.get("documents", [])

    st.session_state.chat_history = chat_history
    st.session_state.pdf_name = documents[-1]["name"] if documents else None
    st.session_state.pdf_indexed = bool(documents)


def reset_to_first_available_conversation():
    conversations = conversation_manager.all()

    if conversations:
        load_conversation(conversations[0])
    else:
        conversation = conversation_manager.create_conversation()
        load_conversation(conversation)


def render_sidebar():
    with st.sidebar:
        st.title("💬 Chats")

        if st.button("➕ Nieuwe chat"):
            conversation = conversation_manager.create_conversation()
            load_conversation(conversation)
            st.rerun()

        st.divider()

        conversations = conversation_manager.all()

        for conversation in conversations:
            chat_id = conversation["id"]
            title = conversation.get("title", "Nieuwe chat")
            is_active = chat_id == st.session_state.conversation_id

            col1, col2 = st.columns([4, 1])

            with col1:
                label = f"👉 {title}" if is_active else title

                if st.button(label, key=f"open_{chat_id}", use_container_width=True):
                    load_conversation(conversation)
                    st.rerun()

            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    conversation_manager.delete_conversation(chat_id)

                    if is_active:
                        reset_to_first_available_conversation()

                    st.rerun()

        st.divider()

        st.title("📄 Document")

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
                document = result["document"]

                conversation_manager.add_document(
                    st.session_state.conversation_id,
                    document,
                )

                st.session_state.pdf_indexed = True
                st.session_state.pdf_name = uploaded_file.name
                st.session_state.chat_history = []

                st.success("PDF opgeslagen en geïndexeerd.")
                st.info(f"Bestand: {file_path.name}")
                st.info(f"Aantal chunks: {chunk_count}")

                st.text_area(
                    "Uitgelezen tekst",
                    pdf_text,
                    height=250,
                )

        st.divider()

        if st.session_state.pdf_indexed:
            st.success(f"Actief document: {st.session_state.pdf_name}")
        else:
            st.warning("Nog geen PDF geïndexeerd.")
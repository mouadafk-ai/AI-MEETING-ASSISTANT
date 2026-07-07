import streamlit as st

from components.sidebar import render_sidebar
from components.chat import render_chat
from components.summary import render_summary
from components.actions import render_actions
from services.conversation_manager import ConversationManager

conversation_manager = ConversationManager()

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide",
)


def messages_to_chat_history(messages):
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

    return chat_history


if "conversation_id" not in st.session_state:
    conversations = conversation_manager.all()

    if conversations:
        st.session_state.conversation_id = conversations[0]["id"]
    else:
        conversation = conversation_manager.create_conversation()
        st.session_state.conversation_id = conversation["id"]

conversation = conversation_manager.get_conversation(
    st.session_state.conversation_id
)

if conversation is None:
    conversation = conversation_manager.create_conversation()
    st.session_state.conversation_id = conversation["id"]

documents = conversation.get("documents", [])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = messages_to_chat_history(
        conversation.get("messages", [])
    )

if "pdf_name" not in st.session_state:
    if documents:
        st.session_state.pdf_name = documents[-1]["name"]
    else:
        st.session_state.pdf_name = None

if "pdf_indexed" not in st.session_state:
    st.session_state.pdf_indexed = bool(st.session_state.pdf_name)

# Sidebar
render_sidebar()

# Header
st.title("🤖 AI Document Assistant")
st.caption("Chat met PDF-documenten, maak samenvattingen en haal actiepunten op.")

st.divider()

# Status cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📄 Document", "1" if st.session_state.pdf_indexed else "0")

with col2:
    st.metric("💬 Vragen", len(st.session_state.chat_history))

with col3:
    st.metric("🧠 RAG", "Actief" if st.session_state.pdf_indexed else "Wachten")

with col4:
    st.metric("✅ Status", "Klaar" if st.session_state.pdf_indexed else "Geen PDF")

st.divider()

# Main dashboard
left_col, right_col = st.columns([2, 1])

with left_col:
    with st.container(border=True):
        render_chat()

with right_col:
    with st.container(border=True):
        st.subheader("📄 Actief document")

        if st.session_state.pdf_indexed:
            st.success(st.session_state.pdf_name)
        else:
            st.warning("Nog geen document geladen.")

    with st.container(border=True):
        render_summary()

    with st.container(border=True):
        render_actions()
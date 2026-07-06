import streamlit as st

from components.sidebar import render_sidebar
from components.chat import render_chat
from components.summary import render_summary
from components.actions import render_actions

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

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = 1

st.title("🤖 AI Meeting Assistant")
st.write("Upload een PDF, indexeer het document en stel vragen over de inhoud.")

render_sidebar()

tab_chat, tab_summary, tab_actions = st.tabs(
    ["💬 Chat", "📝 Samenvatting", "✅ Actiepunten"]
)

with tab_chat:
    render_chat()

with tab_summary:
    render_summary()

with tab_actions:
    render_actions()
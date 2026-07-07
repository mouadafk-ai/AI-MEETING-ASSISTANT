import streamlit as st

from services.rag import ask_question
from services.conversation_manager import ConversationManager

conversation_manager = ConversationManager()


def render_chat():
    st.subheader("💬 Chat")

    chat_box = st.container(height=500)

    with chat_box:
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):
                st.write(chat["answer"])

                if chat.get("sources"):
                    with st.expander("📚 Bronnen"):
                        for source in chat["sources"]:
                            st.write(f"📄 {source['source']}")

    if not st.session_state.pdf_indexed or not st.session_state.pdf_name:
        st.info("Upload en indexeer eerst een PDF in de sidebar.")
        return

    prompt = st.chat_input("Stel een vraag over je document...")

    if prompt:
        with st.spinner("AI zoekt in je document..."):
            result = ask_question(
                question=prompt,
                source=st.session_state.pdf_name,
            )

        chat_item = {
            "question": prompt,
            "answer": result["answer"],
            "sources": result["sources"],
        }

        st.session_state.chat_history.append(chat_item)

        conversation_manager.add_message(
            conversation_id=st.session_state.conversation_id,
            role="user",
            content=prompt,
        )

        conversation_manager.add_message(
            conversation_id=st.session_state.conversation_id,
            role="assistant",
            content=result["answer"],
            sources=result["sources"],
        )

        st.rerun()
import streamlit as st
from services.rag import ask_question


def render_chat():
    st.subheader("💬 Chat")

    if not st.session_state.pdf_indexed or not st.session_state.pdf_name:
        st.info("Upload en indexeer eerst een PDF in de sidebar.")
        return

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

    prompt = st.chat_input("Stel een vraag over je document...")

    if prompt:
        with st.spinner("AI zoekt in je document..."):
            result = ask_question(
                question=prompt,
                source=st.session_state.pdf_name,
            )

        st.session_state.chat_history.append(
            {
                "question": prompt,
                "answer": result["answer"],
                "sources": result["sources"],
            }
        )

        st.rerun()
import streamlit as st

from services.rag import ask_question


def render_chat():
    st.subheader("💬 Stel een vraag over je document")
    st.caption(f"Gesprek #{st.session_state.conversation_id}")

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
                        st.write(f"📄 {source['source']}")
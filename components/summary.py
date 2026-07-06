import streamlit as st

from services.summary import summarize_document


def render_summary():
    st.subheader("📝 Document samenvatten")

    if st.button("Maak samenvatting"):
        if not st.session_state.pdf_indexed:
            st.error("Upload en indexeer eerst een PDF.")
        else:
            with st.spinner("Samenvatting wordt gemaakt..."):
                summary = summarize_document()

            st.markdown(summary)
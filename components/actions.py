import streamlit as st

from services.actions import extract_action_items


def render_actions():
    st.subheader("✅ Actiepunten herkennen")

    if st.button("Haal actiepunten op"):
        if not st.session_state.pdf_indexed:
            st.error("Upload en indexeer eerst een PDF.")
        else:
            with st.spinner("Actiepunten worden gezocht..."):
                actions = extract_action_items()

            st.markdown(actions)
import streamlit as st
from services.loader import save_uploaded_file
from services.pdf_reader import read_pdf

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🤖",
    layout="wide",
)


with st.sidebar:
    st.title("⚙️ Instellingen")
    st.write("Beheer hier je documenten en AI-instellingen.")

    st.divider()

    st.subheader("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload een PDF",
        type=["pdf"]
    )

    st.divider()

    st.subheader("ℹ️ Status")
    st.success("App actief")

    if uploaded_file is not None:
        st.info(f"Geselecteerd bestand: {uploaded_file.name}")

        if st.button("📥 PDF opslaan"):
            file_path = save_uploaded_file(uploaded_file)
            pdf_text = read_pdf(file_path)

            st.success(f"PDF opgeslagen: {file_path}")
            st.text_area("Uitgelezen tekst", pdf_text,height=300)




st.title("🤖 AI Meeting Assistant")
st.write("Analyseer meetings, PDF's en documenten met AI.")

st.divider()

tab_chat, tab_summary, tab_actions = st.tabs(
    ["💬 Chat", "📝 Samenvatting", "✅ Actiepunten"]
)

with tab_chat:
    st.subheader("💬 Stel een vraag over je document")

    user_question = st.text_area(
        "Jouw vraag",
        placeholder="Bijvoorbeeld: Wat zijn de belangrijkste punten uit dit document?",
        height=120,
    )

    if st.button("Vraag stellen", type="primary"):
        if uploaded_file is None:
            st.error("Upload eerst een PDF.")
        elif not user_question:
            st.error("Typ eerst een vraag.")
        else:
            st.info("Hier komt straks het AI-antwoord.")

with tab_summary:
    st.subheader("📝 Document samenvatten")

    if st.button("Maak samenvatting"):
        if uploaded_file is None:
            st.error("Upload eerst een PDF.")
        else:
            st.info("Hier komt straks de samenvatting.")

with tab_actions:
    st.subheader("✅ Actiepunten herkennen")

    if st.button("Haal actiepunten op"):
        if uploaded_file is None:
            st.error("Upload eerst een PDF.")
        else:
            st.info("Hier komen straks de actiepunten.")
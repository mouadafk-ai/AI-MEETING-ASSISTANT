from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from config import CHAT_MODEL
from services.vector_store import get_vector_store

load_dotenv()


def extract_action_items(source: str) -> str:
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(
        query="Zoek alle actiepunten, taken en deadlines.",
        k=10,
        filter={"source": source},
    )

    if not docs:
        return "Ik kon geen tekst vinden voor dit document."

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Je bent een AI Document Assistant.

Haal alle actiepunten uit het document.

Voor elk actiepunt geef:

- ✅ Actie
- 👤 Verantwoordelijke indien bekend
- 📅 Deadline indien genoemd

Als er geen actiepunten zijn, zeg dat duidelijk.

Context:
{context}
"""

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0,
    )

    response = llm.invoke(prompt)

    return response.content
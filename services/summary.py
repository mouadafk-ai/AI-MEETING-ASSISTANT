from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from config import CHAT_MODEL
from services.vector_store import get_vector_store

load_dotenv()


def summarize_document(source: str) -> str:
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(
        query="Geef een algemene samenvatting van het document.",
        k=10,
        filter={"source": source},
    )

    if not docs:
        return "Ik kon geen tekst vinden voor dit document."

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Je bent een AI Document Assistant.

Maak een professionele samenvatting van het document.

Gebruik deze structuur:

## 📄 Onderwerp

## 📝 Samenvatting

## 📌 Belangrijkste punten

## ⚠️ Belangrijke informatie

Context:
{context}
"""

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0,
    )

    response = llm.invoke(prompt)

    return response.content
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from config import CHAT_MODEL, TOP_K_RESULTS
from services.vector_store import get_vector_store

load_dotenv()


def ask_question(question: str, source: str) -> dict:
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(
        query=question,
        k=TOP_K_RESULTS,
        filter={"source": source},
    )

    if not docs:
        return {
            "answer": "Ik kon geen relevante informatie vinden in dit document.",
            "sources": [],
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Je bent een AI Document Assistant.

Beantwoord de vraag alleen op basis van de onderstaande context.
Als het antwoord niet in de context staat, zeg dan eerlijk dat je het niet weet.

Context:
{context}

Vraag:
{question}

Antwoord:
"""

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0,
    )

    response = llm.invoke(prompt)

    sources = []
    seen_sources = set()

    for doc in docs:
        doc_source = doc.metadata.get("source", "Onbekend")

        if doc_source not in seen_sources:
            sources.append({"source": doc_source})
            seen_sources.add(doc_source)

    return {
        "answer": response.content,
        "sources": sources,
    }
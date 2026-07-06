"""
Alle instellingen staan op één plek.
"""

# OpenAI
CHAT_MODEL = "gpt-5-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ChromaDB
COLLECTION_NAME = "meeting_documents"
VECTOR_DB_PATH = "vector_db"

# Retrieval
TOP_K_RESULTS = 3
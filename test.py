from src.services.embeddings import (
    EMBEDDING_DIMENSION,
    embed_text,
)


text = """
Our backend services use Python and FastAPI.
We use PostgreSQL for relational data and Redis
for caching and conversation memory.
"""


vector = embed_text(text)

print("Embedding dimension:", len(vector))
print("Expected dimension:", EMBEDDING_DIMENSION)
print("First 10 values:", vector[:10])
print("All values are floats:", all(isinstance(x, float) for x in vector))
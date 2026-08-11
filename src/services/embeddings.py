from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    """

    return SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding for one text.
    """

    if not text.strip():
        raise ValueError(
            "Cannot generate an embedding for empty text."
        )

    model = get_embedding_model()

    vector = model.encode(
        text,
        normalize_embeddings=True,
    )

    return vector.tolist()


def embed_texts(
    texts: list[str],
) -> list[list[float]]:
    """
    Generate embeddings for multiple texts.
    """

    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError(
            "Cannot generate embeddings for empty text."
        )

    model = get_embedding_model()

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return vectors.tolist()
from dataclasses import dataclass

from src.services.embeddings import embed_text
from src.services.vector_store import search


@dataclass(slots=True)
class RetrievedChunk:
    id: str
    document_id: str | None
    filename: str | None
    chunk_index: int | None
    text: str
    section: str | None


def retrieve(
    query: str,
    limit: int = 5,
) -> list[RetrievedChunk]:
    """
    Retrieve the top matching document chunks for a query.

    Retrieval is performed across all uploaded documents
    using vector similarity only.
    """

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    if limit <= 0:
        raise ValueError("limit must be greater than zero.")

    query_vector = embed_text(query)

    results = search(
        vector=query_vector,
        limit=limit,
    )

    return [
        RetrievedChunk(
            id=result["id"],
            document_id=result.get("document_id"),
            filename=result.get("filename"),
            chunk_index=result.get("chunk_index"),
            text=result.get("text") or "",
            section=result.get("section"),
        )
        for result in results
    ]


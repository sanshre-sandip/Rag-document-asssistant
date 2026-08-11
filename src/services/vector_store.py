from functools import lru_cache
from uuid import UUID

import weaviate
from weaviate.classes.config import Configure, DataType, Property

from src.config import weaviate_cluster_api_key, weaviate_cluster_url


COLLECTION_NAME = "DocumentChunk"


@lru_cache(maxsize=1)
def get_weaviate_client():
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_cluster_url,
        auth_credentials=weaviate_cluster_api_key,
    )


def ensure_collection() -> None:
    client = get_weaviate_client()

    if client.collections.exists(COLLECTION_NAME):
        return

    client.collections.create(
        name=COLLECTION_NAME,
        vector_config=Configure.Vectors.self_provided(),
        properties=[
            Property(
                name="document_id",
                data_type=DataType.TEXT,
            ),
            Property(
                name="filename",
                data_type=DataType.TEXT,
            ),
            Property(
                name="chunk_index",
                data_type=DataType.INT,
            ),
            Property(
                name="text",
                data_type=DataType.TEXT,
            ),
            Property(
                name="section",
                data_type=DataType.TEXT,
            ),
        ],
    )


def insert_chunks(
    document_id: UUID,
    filename: str,
    chunks: list[dict],
) -> list[str]:
    """
    Insert document chunks and their pre-generated vectors
    into Weaviate.
    """

    if not chunks:
        return []

    ensure_collection()

    client = get_weaviate_client()
    collection = client.collections.get(COLLECTION_NAME)

    ids: list[str] = []

    with collection.batch.dynamic() as batch:
        for chunk in chunks:
            object_id = batch.add_object(
                properties={
                    "document_id": str(document_id),
                    "filename": filename,
                    "chunk_index": chunk["index"],
                    "text": chunk["text"],
                    "section": chunk.get("section"),
                },
                vector=chunk["vector"],
            )

            ids.append(str(object_id))

    return ids


def search(
    vector: list[float],
    limit: int = 5,
) -> list[dict]:
    """
    Search Weaviate using a pre-generated query vector.
    """

    ensure_collection()

    client = get_weaviate_client()
    collection = client.collections.get(COLLECTION_NAME)

    response = collection.query.near_vector(
        near_vector=vector,
        limit=limit,
    )

    results = []

    for obj in response.objects:
        results.append(
            {
                "id": str(obj.uuid),
                "document_id": obj.properties.get(
                    "document_id"
                ),
                "filename": obj.properties.get(
                    "filename"
                ),
                "chunk_index": obj.properties.get(
                    "chunk_index"
                ),
                "text": obj.properties.get(
                    "text"
                ),
                "section": obj.properties.get(
                    "section"
                ),
            }
        )

    return results
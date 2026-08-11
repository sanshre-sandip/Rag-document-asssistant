from functools import lru_cache
from uuid import UUID

import weaviate
from weaviate.classes.config import Configure, Property, DataType

from src.config import weaviate_cluster_api_key, weaviate_cluster_url


COLLECTION_NAME = "DocumentChunk"


@lru_cache(maxsize=1)
def get_weaviate_client():
    """
    Create and cache the Weaviate Cloud client.
    """

    return weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_cluster_url,
        auth_credentials=weaviate_cluster_api_key,
    )


def close_weaviate_client() -> None:
    """
    Close the cached Weaviate client.
    """

    client = get_weaviate_client()
    client.close()


def ensure_collection() -> None:
    """
    Create the DocumentChunk collection if it does not exist.

    Vectors are provided by our local
    sentence-transformers model, so Weaviate
    performs no automatic vectorization.
    """

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


def insert_chunk(
    document_id: UUID,
    filename: str,
    chunk_index: int,
    text: str,
    section: str | None,
    vector: list[float],
) -> str:

    ensure_collection()

    client = get_weaviate_client()
    collection = client.collections.get(
        COLLECTION_NAME
    )

    properties = {
        "document_id": str(document_id),
        "filename": filename,
        "chunk_index": chunk_index,
        "text": text,
        "section": section,
    }

    uuid = collection.data.insert(
        properties=properties,
        vector=vector,
    )

    return str(uuid)


def search(
    vector: list[float],
    limit: int = 5,
) -> list[dict]:

    ensure_collection()

    client = get_weaviate_client()
    collection = client.collections.get(
        COLLECTION_NAME
    )

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
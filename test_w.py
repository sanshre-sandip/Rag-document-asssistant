from src.services.vector_store import (
    COLLECTION_NAME,
    ensure_collection,
    get_weaviate_client,
)


client = get_weaviate_client()

print("Connected:", client.is_ready())

ensure_collection()

print("Collection:", COLLECTION_NAME)
print(
    "Exists:",
    client.collections.exists(COLLECTION_NAME),
)

client.close()
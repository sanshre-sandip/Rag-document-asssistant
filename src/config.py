import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
weaviate_cluster_url = os.getenv("WEAVIATE_CLUSTER_URL")
weaviate_cluster_api_key = os.getenv("WEAVIATE_API_KEY")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

if not weaviate_cluster_url and not weaviate_cluster_api_key:
    raise RuntimeError("Vector db not configured in .env")


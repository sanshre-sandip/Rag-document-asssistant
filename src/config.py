import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
weaviate_cluster_url = os.getenv("WEAVIATE_CLUSTER_URL")
weaviate_cluster_api_key = os.getenv("WEAVIATE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
groq_base_url = os.getenv("GROQ_BASE_URL")
model = os.getenv("MODEL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

if not weaviate_cluster_url and not weaviate_cluster_api_key:
    raise RuntimeError("Vector db not configured in .env")

if not groq_api_key and not groq_base_url and not model:
    raise RuntimeError("llm not configured in .env")


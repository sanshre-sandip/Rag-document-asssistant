import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API")
GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
)
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant",
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set in .env"
    )

if not WEAVIATE_CLUSTER_URL:
    raise RuntimeError(
        "WEAVIATE_CLUSTER_URL is not set in .env"
    )

if not WEAVIATE_API_KEY:
    raise RuntimeError(
        "WEAVIATE_API_KEY is not set in .env"
    )

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set in .env"
    )
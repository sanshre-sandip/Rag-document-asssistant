from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Conversational RAG"],
)


@router.get("/health")
async def chat_health() -> dict[str, str]:
    return {
        "service": "conversational-rag",
        "status": "ok",
    }
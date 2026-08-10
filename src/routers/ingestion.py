from fastapi import APIRouter



router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Document Ingestion"],
)



@router.get("/health")
async def ingestion_health() -> dict[str, str]:
    return {
        "service": "document-ingestion",
        "status": "ok",
    }
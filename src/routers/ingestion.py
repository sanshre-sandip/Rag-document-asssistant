from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.models import Document
from src.db.models import (
    ChunkResponse,
    DocumentIngestionResponse,
)
from src.services.chunking import (
    ChunkingStrategy,
    chunk_text,
)
from src.services.extractor import (
    DocumentExtractionError,
    extract_text,
)


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


@router.post(
    "/ingest",
    response_model=DocumentIngestionResponse,
)
async def ingest_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.STRUCTURE_AWARE,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    db: AsyncSession = Depends(get_db),
) -> DocumentIngestionResponse:

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    extension = file.filename.lower().rsplit(".", 1)[-1]

    if extension not in {"pdf", "txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    if chunk_size <= 0:
        raise HTTPException(
            status_code=400,
            detail="chunk_size must be greater than zero.",
        )

    if chunk_overlap < 0:
        raise HTTPException(
            status_code=400,
            detail="chunk_overlap cannot be negative.",
        )

    if chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=400,
            detail="chunk_overlap must be smaller than chunk_size.",
        )

    try:
        text = await extract_text(file)

    except DocumentExtractionError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    try:
        chunks = chunk_text(
            text=text,
            strategy=chunking_strategy,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No chunks were generated from the document.",
        )

    document = Document(
        filename=file.filename,
        content_type=file.content_type,
        source="upload",
    )

    db.add(document)

    await db.commit()
    await db.refresh(document)

    return DocumentIngestionResponse(
        document_id=document.id,
        filename=document.filename,
        content_type=document.content_type,
        chunking_strategy=chunking_strategy,
        chunk_count=len(chunks),
        chunks=[
            ChunkResponse(
                index=chunk.index,
                text=chunk.text,
                section=chunk.section,
            )
            for chunk in chunks
        ],
    )
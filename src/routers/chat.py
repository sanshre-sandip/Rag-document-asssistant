from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.services.memory import (
    add_message,
    get_history,
)
from src.services.rag import answer_question

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Conversational RAG"],
)


class ChatRequest(BaseModel):
    conversation_id: str = Field(
        ...,
        min_length=1,
        description="Conversation identifier",
    )

    message: str = Field(
        ...,
        min_length=1,
        description="User's question",
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve",
    )


class ChatSource(BaseModel):
    document_id: str | None
    filename: str | None
    section: str | None
    chunk_index: int | None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]


@router.get("/health")
async def chat_health() -> dict[str, str]:
    return {
        "service": "conversational-rag",
        "status": "ok",
    }


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:

    try:
        history = get_history(
            request.conversation_id,
        )

        answer, chunks = answer_question(
            query=request.message,
            limit=request.limit,
            history=history,
        )

        add_message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
        )

        add_message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=answer,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response.",
        ) from exc

    sources = [
        ChatSource(
            document_id=chunk.document_id,
            filename=chunk.filename,
            section=chunk.section,
            chunk_index=chunk.chunk_index,
        )
        for chunk in chunks
    ]

    return ChatResponse(
        answer=answer,
        sources=sources,
    )
